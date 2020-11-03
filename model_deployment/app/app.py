import pickle
from flask import Flask, request, redirect
from flasgger import Swagger
import numpy as np
import pandas as pd
import sqlite3


# with open('/var/www/app/randomforest.pki', 'rb') as model_file:
#     model = pickle.load(model_file)

# database connection
try:
    sqliteConnection = sqlite3.connect('./model/iris.db')
    cursor = sqliteConnection.cursor()
except Exception as e:
    print(str(e))

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def home():
    return redirect('/apidocs')

@app.route('/train')
def train_model(feature_table='features', target_table='target', conn=sqliteConnection):
    """Train model using data from database and save train model as a binary file using pickle
    ---
    parameters:
     
    """
    pass 




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)