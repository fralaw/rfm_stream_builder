"""
// Name        : LogisticRegression.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe concreta LogisticRegression che eredita da IncrementalClassifier.
"""
import pandas as pd
from river import linear_model
from ClassifierInterface import ClassifierInterface


class LogisticRegression(ClassifierInterface):
    def __init__(self):
        self.__model = linear_model.LogisticRegression()

    def learn(self, x: pd.DataFrame, y: pd.Series):
        # orient="records" genera una lista dove ogni elemento è una riga del DataFrame sotto forma di dizionario
        self.__model = self.__model.learn_many(x, y)
        return self

    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        # orient="records" genera una lista dove ogni elemento è una riga del DataFrame sotto forma di dizionario
        return self.__model.predict_many(x)

    def predict_one(self, x: pd.Series) -> bool:
        return self.__model.predict_one(x)