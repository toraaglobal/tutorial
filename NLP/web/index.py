#https://kanoki.org/2020/07/18/python-api-documentation-using-flask-swagger/
#https://www.udemy.com/course/deploy-data-science-nlp-models-with-docker-containers/
import json,os
import logging
import sys
import config
import requests
import pandas as pd 
import numpy as np 
from flask import Flask, request, Response, jsonify,make_response, send_file
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from
from waitress import serve
from stemming.porter2 import stem
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from io import BytesIO
import time
import zipfile



app = Flask(__name__)
app.config.from_object(config.Config)
api = Api(app)

# Create an APISpec
template = {
  "swagger": "2.0",
  "info": {
    "title": "Unstructure Text Clustering - API",
    "description": "Unstructure text clustering using kmeans",
    "version": "0.1.1",
    "contact": {
      "name": "Tajudeen Abdulazeez",
      "url": "https://www.toraaglobal.com/",
    }
  },
  "securityDefinitions": {
    "Bearer": {
      "type": "apiKey",
      "name": "Authorization",
      "in": "header",
      "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
    }
  },
  "security": [
    {
      "Bearer": [ ]
    }
  ]

}

app.config['SWAGGER'] = {
    'title': 'Sentiment Analysis',
    'uiversion': 3,
    "specs_route": "/"
}
swagger = Swagger(app, template= template)
app.config.from_object(config.Config)
api = Api(app)



class Cluster(Resource):

    @staticmethod
    def cleanse_text(text:str)->str:
        if text:
            #whitespaces
            clean = ' '.join(text.split())
            
            # Stemming
            red_text = [stem(word) for word in clean.split()]
            
            # Done. return
            return ' '.join(red_text)

        else:
            return text

    def post(self):
        """
        cluster unstructure text
        ---
        parameters:
            - name: col
              in: query
              type: string 
              required: false
              description: column name
            - name: no_of_clusters
              in: query
              type: number
              required: false
              description: number of clusters
            - name: datasets
              in: formData
              type: file
              required: true
              description: csv file with the unstructure text
        responses:
            500:
                description: Bad imputs, check API documentation for required params
            200:
                description: Cluster results in excel file
               
        """
        data = pd.read_csv(request.files.get('datasets'))
        unstructure = 'text'
        if 'col' in request.args:
            unstructure = request.args.get('col')

        no_of_clusters = 2
        if 'no_of_clusters' in request.args:
            no_of_clusters = int(request.args.get('no_of_clusters'))

        data = data.fillna('NULL')

        data['clean_sum'] = data[unstructure].apply(cleanse_text)

        vectorizer = CountVectorizer(analyzer='word',
                                 stop_words='english')
        counts = vectorizer.fit_transform(data['clean_sum'])
        
        kmeans = KMeans(n_clusters=no_of_clusters)

        data['cluster_num'] = kmeans.fit_predict(counts)
        data = data.drop(['clean_sum'], axis=1)

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        data.to_excel(writer, sheet_name='Clusters', 
                  encoding='utf-8', index=False)

        clusters = []
        for i in range(np.shape(kmeans.cluster_centers_)[0]):
            data_cluster = pd.concat([pd.Series(vectorizer.get_feature_names()),
                                    pd.DataFrame(kmeans.cluster_centers_[i])],
            axis=1)
            data_cluster.columns = ['keywords', 'weights']
            data_cluster = data_cluster.sort_values(by=['weights'], ascending=False)
            data_clust = data_cluster.head(n=10)['keywords'].tolist()
            clusters.append(data_clust)
        pd.DataFrame(clusters).to_excel(writer, sheet_name='Top_Keywords', encoding='utf-8')

        #Pivot
        data_pivot = data.groupby(['cluster_num'], as_index=False).size()
        data_pivot.name = 'size'
        data_pivot = data_pivot.reset_index()
        data_pivot.to_excel(writer, sheet_name='Cluster_Report', 
                    encoding='utf-8', index=False)

        # insert chart
        workbook = writer.book
        worksheet = writer.sheets['Cluster_Report']
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
                'values': '=Cluster_Report!$B$2:$B'+str(no_of_clusters+1)
                })
        worksheet.insert_chart('D2', chart)
        
        writer.save()

        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            names = ['cluster_output.xlsx']
            files = [output]
            for i in range(len(files)):
                data = zipfile.ZipInfo(names[i])
                data.date_time = time.localtime(time.time())[:6]
                data.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(data, files[i].getvalue())
        memory_file.seek(0)
        response = make_response(send_file(memory_file, attachment_filename='cluster_output.zip',
                                        as_attachment=True))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response




## Api resource routing
api.add_resource(Cluster, '/cluster')

if __name__ == "__main__":
    serve(app, host='0.0.0.0',port=5000)
    
  