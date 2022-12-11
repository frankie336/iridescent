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



data = "output/feature_extraction.csv"

def classify(data):
    # Read the data into a dataframe
    df = pd.read_csv(data)

    features_list = df.columns.to_list()
    remove_list = ["Unnamed: 0","programmer","contest","round"]
    features_list = [x for x in features_list if x not in remove_list]



    """
    ASTNodeBigramsT
    """
    # Convert the ASTNodeBigramsTF column into a list of bigram counts
    bigram_counts = [Counter(text.split()) for text in df["ASTNodeBigramsTF"]]

    # Convert the bigram counts to a list of floats
    bigram_counts_floats = [[float(count) for count in bc.values()] for bc in bigram_counts]


    df['counts_ASTNodeBigramsTF'] = ""

    for i in range(len(df)):
        df.loc[i, "counts_ASTNodeBigramsTF"] = df.loc[i, "counts_ASTNodeBigramsTF"] + str(bigram_counts_floats[i])

    df = df.drop(columns=["ASTNodeBigramsTF"])
    df.rename({'counts_ASTNodeBigramsTF': 'ASTNodeBigramsTF'}, axis=1, inplace=True)

    """
    WordUnigramTF
    """
    # Convert the WordUnigramTF column into a list of WordUnigramTF counts
    WordUnigramTF_counts = [Counter(text.split()) for text in df["WordUnigramTF"]]

    # Convert the WordUnigramTF_counts counts to a list of floats
    WordUnigramTF_counts_floats = [[float(count) for count in bc.values()] for bc in WordUnigramTF_counts]

    df['counts_WordUnigramTF'] = ""

    for i in range(len(df)):
        df.loc[i, "counts_WordUnigramTF"] = df.loc[i, "counts_WordUnigramTF"] + str(WordUnigramTF_counts_floats[i])

    df = df.drop(columns=["WordUnigramTF"])
    df.rename({"counts_WordUnigramTF": "WordUnigramTF"}, axis=1, inplace=True)


    df["WordUnigramTF"] = df["WordUnigramTF"].str.replace("[", "")
    df["WordUnigramTF"] = df["WordUnigramTF"].str.replace("]", "")
    df["WordUnigramTF"] = df["WordUnigramTF"].str.replace(",", " ")
    df["ASTNodeBigramsTF"] = df["ASTNodeBigramsTF"].str.replace("[", "")
    df["ASTNodeBigramsTF"] = df["ASTNodeBigramsTF"].str.replace("]", "")
    df["ASTNodeBigramsTF"] = df["ASTNodeBigramsTF"].str.replace(",", " ")

    df['WordUnigramTF'] = pd.to_numeric(df['WordUnigramTF'], errors='coerce')
    df['ASTNodeBigramsTF'] = pd.to_numeric(df['ASTNodeBigramsTF'], errors='coerce')
    df.fillna(0, inplace=True)



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



