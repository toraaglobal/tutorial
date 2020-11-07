# How to deploy a production ready machine learning model?
Four step to Deploy a deep learning model using docker container and flask API
***

In this article, I will illustrate a 4-step  to deploy a deep learning model using  flask API and docker container. Waitress package manage user concurrency should wanted to use in production.

Here is the URL of the model we will build and deploy on heroku with details step by step guide.

Project link on github : `https://github.com/toraaglobal/tutorial/tree/machine_learning/NLP`

### Why docker container?
* its easy to reproduce in different environment
* isolation portability
* Scalibility


Our folder structure will look like this:

![](./model/folder_structure.png)

### Step 1 : Build a machine machine learning model
In real world, we will need to train and optimized our hyperparameters for the best performance we are tring to solve. for this example, we will be using a base line deep learning model and the mnist datasets.

create a python file called `train_model.py` to train and save the model.

```
from keras.datasets import mnist
import matplotlib. pyplot as plt
import numpy
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')

# Load dataset (download if needed)
(X_train, y_train), (X_test, y_test) = mnist.load_data()

plt.subplot(221)
plt.imshow(X_train[0], cmap=plt.get_cmap('gray'))
plt.subplot(222)
plt.imshow(X_train[1], cmap=plt.get_cmap('gray'))
plt.subplot(223)
plt.imshow(X_train[2], cmap=plt.get_cmap('gray'))
plt.subplot(224)
plt.imshow(X_train[3], cmap=plt.get_cmap('gray'))

plt.show()


# fix the seed 
seed = 7
numpy.random.seed(seed)

X_train = X_train.reshape(X_train.shape[0], 1, 28, 28).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 1, 28, 28).astype('float32')

X_train = X_train / 255
X_test = X_test / 255

# one hot encoding
# output - [ 0 0 0 0 0 1 0 0 0 0 ]
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

num_classes = y_train.shape[1]


def baseline_model():
    model = Sequential()
    model.add(Conv2D(8, (3,3), input_shape=(1,28,28), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    
    model.add(Flatten())
    model.add(Dense(4, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])
    
    return model

# build a model
model = baseline_model()

# Fit 
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10,
          batch_size=32, verbose=2)

model.save('./model/model.h5')

# Final eval
scores = model.evaluate(X_test, y_test, verbose=0)
print("CNN error: %.2f%%" % (100 - scores[1]*100))


```

the model is saved in the `model` folder and will be use to make prediction using the flask api


The next step is to create the flask API



### Step 2 : Create a flask Application
create a flask application using flasgger to document the API.
The flask application serve with waitress package  to manage concurrency.

create a file `index.py`

```
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
    
  

```



### Step 3: Put all the application in a docker countainer
create a requirements.txt 
```
flask
flasgger
scikit-learn==0.18.1
waitress
config
flask_restful
stemming

```

create a `Dockerfile` and place it in the root folder. check folder structure for details

```
FROM continuumio/anaconda3:4.4.0
LABEL name="Tajudeen Abdulazeez" email="tabdulazeez99@gmail.com" version="1.0"
EXPOSE 5000

WORKDIR /web/
COPY ./web /web/

RUN pip install -r requirements.txt 
RUN conda install -c conda-forge keras
RUN pip install -Iv tensorflow_estimator==1.13.0
RUN python train_model.py
   
CMD ["python", "index.py"]
```

create a `start_application.sh` file to start the application

```
#!/bin/bash
sudo docker build -t nlpapi . && sudo docker run -p 5000:5000 --name nlpapi -d nlpapi && sudo docker inspect nlpapi


```

create a `stop_application.sh` file to stop the application in the dev environment


starting the application
```
bash start_application.sh
```

go to `localhost:5000` to access the API

To stop the application:

```
bash stop_application.sh
```


### Step 4: deploy the application on heroku
Install the Heroku CLI

`https://devcenter.heroku.com/articles/heroku-cli#download-and-install`

Download and install the Heroku CLI.

Create `heroku.yml` file in the root directory:
```
build:
  docker:
    web: Dockerfile
```

commit the file to the repo
```
git add heroku.yml

git commit -m "Add heroku.yml"
```

set stack of the container
```
heroku stack:set container
```
push your application to master

```
git push heroku master
```


**Deploy using docker registry**

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

```
heroku login
```

Log in to Container Registry

You must have Docker set up locally to continue. You should see output when you run this command.

```
docker ps
```

Now you can sign into Container Registry.

```
heroku container:login
```

Push your Docker-based app

Build the Dockerfile in the current directory and push the Docker image.

```
heroku container:push web
```

Deploy the changes

Release the newly pushed images to deploy your app.

```
heroku container:release web
```


**References**

https://www.udemy.com/course/deploy-data-science-nlp-models-with-docker-containers/

https://kanoki.org/2020/07/18/python-api-documentation-using-flask-swagger/


