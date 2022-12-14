import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import numpy as np
from sklearn.model_selection import train_test_split
#Import Random Forest Model
from sklearn.ensemble import RandomForestClassifier
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
from collections import Counter


data = "output/feature_extraction.csv"



# Define a function to check if an element is suitable for a dictionary value
def is_dict_value(x):
    return x is not None and not isinstance(x, (list, dict))



def classify(data):
    # Read the data into a dataframe
    df = pd.read_csv(data)

    print(df.columns)
    print(df.shape)

    features_list = df.columns.to_list()
    remove_list = ["Unnamed: 0","programmer","contest","round"]
    features_list = [x for x in features_list if x not in remove_list]



    df = df.drop(columns=["contest", "round"])
    categorical_columns = ["programmer"]
    for column in categorical_columns:
        df[column] = pd.factorize(df[column])[0]


    cols = list(df.columns.values)
    x = df[cols[1:]]
    y = df[['programmer']]

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)  # 70% training and 30% test

    # Create a Gaussian Classifier
    clf = RandomForestClassifier(n_estimators=100)

    for i in range(100):
        clf.fit(X_train, y_train.values.ravel())
        y_pred = clf.predict(X_test)
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))




classify(data)



