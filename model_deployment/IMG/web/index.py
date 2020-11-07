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
from keras.models import load_model
from PIL import Image
import numpy as np



app = Flask(__name__)
app.config.from_object(config.Config)
api = Api(app)

model = load_model('./model/model.h5')

# Create an APISpec
template = {
  "swagger": "2.0",
  "info": {
    "title": "Digit Recognition - API",
    "description": "returning a prediction of mnist dataset",
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
    'title': 'deep learning',
    'uiversion': 3,
    "specs_route": "/"
}
swagger = Swagger(app, template= template)
app.config.from_object(config.Config)
api = Api(app)


class DigitRecognition(Resource):
    def post():
        """
        prediction of mnist
        ---
        parameters:
            - name: image
              in: formData
              type: file
              required: true

        responses:
            500:
                description: Bad input... use mnist dataset for prediction
            200:
                description: success
                schema:
                    parameters:
                        result:
                            type: string
                            description: the prediction of input image

        """
        im = Image.open(request.files['image'])
        im2arr = np.array(im).reshape((1, 1, 28, 28))
        return str(np.argmax(model.predict(im2arr)))
        

## Api resource routing
api.add_resource(DigitRecognition, '/digit')

if __name__ == "__main__":
    serve(app, host='0.0.0.0',port=5000)
    
  