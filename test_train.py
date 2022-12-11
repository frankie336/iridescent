import time

import pandas as pd

from sklearn.model_selection import train_test_split
#Import Random Forest Model
from sklearn.ensemble import RandomForestClassifier
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics


# Use numpy to convert to arrays
import numpy as np
def data_science():

    """
    1. Open the .csv as df
    2. drop unknown columns
    """
    df = pd.read_csv('output/feature_extraction.csv')
    df = df.drop(columns=["contest", "round"])
    df = pd.get_dummies(df, columns=['ASTNodeBigramsTF','WordUnigramTF'])


    categorical_columns = ['programmer']
    for column in categorical_columns:
        df[column] = pd.factorize(df[column])[0]


    #df['programmer'] = df['programmer'].astype('category')

    #print(df.dtypes)

    #time.sleep(1000)
    #df['programmer'] = 'gennady.korotkevich'

    """
    1. convert programmer names to dtype cats
    2. make a new column from the cat codes 
    """

    cols = list(df.columns.values)
    x = df[cols[1:]]
    y = df[['programmer']]

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)  # 70% training and 30% test

    # Create a Gaussian Classifier
    clf = RandomForestClassifier(n_estimators=100)



    for i in range(10):
        clf.fit(X_train, y_train.values.ravel())
        y_pred = clf.predict(X_test)
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))



data_science()






