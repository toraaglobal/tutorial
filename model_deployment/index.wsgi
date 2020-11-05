#! /usr/bin/python

import sys
import os 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

sys.path.insert(0, "/var/www/app")
sys.path.insert(0, "/opt/conda/lib/python3.6/site-packages")
sys.path.insert(0, "/opt/conda/bin/")

os.environ['PYTHONPATH'] = '/opt/conda/bin/python'

from app import app as application 