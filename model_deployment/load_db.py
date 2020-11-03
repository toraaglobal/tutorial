import pandas as pd 
import numpy as np 
import sqlite3
from sklearn.datasets import load_iris

# connect to database
try:
    sqliteConnection = sqlite3.connect('./app/model/iris.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")
    # load iris datasets
    iris = load_iris()
    features = iris.data 
    target = iris.target 
    columns = iris.feature_names 

    # create a pandas data frame
    df = pd.DataFrame(data=features, columns=columns)

    df.to_sql('features',sqliteConnection,if_exists='fail', index=False)

    # select from database
    cursor.execute("select * from features")
    data = cursor.fetchall()
    print(data)

    # use pandas to load data from database
    data = pd.read_sql("select * from features",sqliteConnection)
    print(data.head())

    # load target to database
    x = pd.DataFrame(data=target, columns=['target'])
    x.to_sql('target',sqliteConnection,if_exists='fail', index=False)

    # read target from database
    tg = pd.read_sql("select * from target", sqliteConnection)
    print(tg.head())
    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("The SQLite connection is closed")




