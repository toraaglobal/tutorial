#https://kanoki.org/2020/07/18/python-api-documentation-using-flask-swagger/
import json,os
import logging
import sys
import config
import requests
import pandas as pd 
import numpy as np 
from flask import Flask, request, Response, jsonify
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from
from waitress import serve

app = Flask(__name__)
app.config.from_object(config.Config)
api = Api(app)

# Create an APISpec
template = {
  "swagger": "2.0",
  "info": {
    "title": "Sentiment Analysis - API",
    "description": "An API for sentiment analysis",
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


class Todo(Resource):
    def get(self):
      """
      post endpoint
      ---      
      tags:
        - Restful APIs
      parameters:
        - name: a
          in: query
          type: integer
          required: true
          description: first number
        - name: b
          in: query
          type: integer
          required: true
          description: second number
      responses:
        500:
          description: Error The number is not integer!
        200:
          description: Number statistics
          schema:
            id: stats
            properties:
              sum:
                type: integer
                description: The sum of number
              product:
                type: integer
                description: The sum of number
              division:
                type: integer
                description: The sum of number              
      """
      
      a = int(request.args.get("a"))
      b = int(request.args.get("b"))
      numsum = a+b
      prod = a*b
      div = a/b
      return jsonify({
                "sum": numsum,
                "product": prod,
                "division": div
            })
        


## Api resource routing
api.add_resource(Todo, '/stats')

if __name__ == "__main__":
    serve(app, host='0.0.0.0',port=5000)
    
  