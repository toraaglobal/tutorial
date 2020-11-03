import pandas as pd 
import numpy as np 
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# make a connection to database
try:
    sqliteConnection = sqlite3.connect('./app/model/iris.db')
    cursor = sqliteConnection.cursor()
except Exception as e:
    print(str(e))

# get data from database
data = pd.read_sql("select * from features",sqliteConnection)
target = pd.read_sql("select * from target",sqliteConnection)

print(data.head())
print(target.head())

X = data.values
y = target.values

# train test split
X_train,X_test, y_train, y_test = train_test_split(X,y,test_size=0.7)

# model
rf = RandomForestClassifier(n_estimators=10)  # initialize model
rf.fit(X_train,y_train)  # fit model

prediction = rf.predict(X_test)
score = accuracy_score(prediction, y_test)
print("accuracy score : {}".format(score))

# save model
with open('./app/model/randomforest.pki','wb') as model:
    pickle.dump(rf, model, protocol=2)



