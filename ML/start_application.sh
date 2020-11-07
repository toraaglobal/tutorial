#!/bin/bash
sudo docker build -t nlpapi . && sudo docker run -p 5000:5000 --name nlpapi -d nlpapi && sudo docker inspect nlpapi
