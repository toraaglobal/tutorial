import pickle
from flask import Flask, request, redirect
from flasgger import Swagger
import numpy as np
import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle


# database connection
try:
    sqliteConnection = sqlite3.connect('./model/iris.db')
    cursor = sqliteConnection.cursor()
except Exception as e:
    print(str(e))

def train_model(n_estimators=10,test_size=0.7):
    data = pd.read_sql("select * from features",sqliteConnection)
    target = pd.read_sql("select * from target",sqliteConnection)

    X = data.values
    y = target.values

    # train test split
    X_train,X_test, y_train, y_test = train_test_split(X,y,test_size=test_size)
    model = RandomForestClassifier(n_estimators=n_estimators)  # initialize model
    model.fit(X_train,y_train)  # fit model

    prediction = model.predict(X_test)
    score = accuracy_score(prediction, y_test)
    # save model
    with open('randomforest.pki','wb') as model_rf:
        pickle.dump(model_rf, model, protocol=2)
    return score 

_ = train_model(n_estimators=10,test_size=0.7)

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def home():
    return redirect('/apidocs')

@app.route('/train')
def re_train_model(n_estimators=10,test_size=0.7):
    """Train model using data from database and save train model as a binary file using pickle
    ---
    parameters:
     - name: n_estimators
       in: query
       type: number
       required: true 

     - name: test_size
       in: query
       type: number
       required: true
    """
    score = train_model(n_estimators,test_size)
    return str("Model Accuracy : {}".format(score))


@app.route('/predict')
def predict_iris():
    """Example endpoint returning a prediction of iris
    ---
    parameters:
      - name: s_length
        in: query
        type: number
        required: true
      - name: s_width
        in: query
        type: number
        required: true
      - name: p_length
        in: query
        type: number
        required: true
      - name: p_width
        in: query
        type: number
        required: true
    """
    with open('randomforest.pki','rb') as model_file:
        model = pickle.load(model_file)

    s_length = request.args.get("s_length")
    s_width = request.args.get("s_width")
    p_length = request.args.get("p_length")
    p_width = request.args.get("p_width")
    prediction = model.predict(np.array([[s_length, s_width, p_length, p_width]]))
    return str(prediction)


@app.route('/predict_file', methods=["POST"])
def predict_iris_file():
    """Example file endpoint returning a prediction of iris
    ---
    parameters:
      - name: input_file
        in: formData
        type: file
        required: true
    """
    with open('randomforest.pki','rb') as model_file:
        model = pickle.load(model_file)

    input_data = pd.read_csv(request.files.get("input_file"), header=None)
    prediction = model.predict(input_data)
    return str(list(prediction))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)