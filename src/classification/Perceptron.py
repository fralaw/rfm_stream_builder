"""
// Name        : Perceptron.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe concreta Perceptron che eredita da IncrementalClassifier.
"""
import pandas as pd
from river import linear_model
from ClassifierInterface import ClassifierInterface


class Perceptron(ClassifierInterface):
    def __init__(self):
        self.__model = linear_model.Perceptron()

    def learn(self, x: pd.DataFrame, y: pd.Series):
        # orient="records" genera una lista dove ogni elemento è una riga del DataFrame sotto forma di dizionario
        self.__model.learn_many(x, y)

    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        # orient="records" genera una lista dove ogni elemento è una riga del DataFrame sotto forma di dizionario
        return self.__model.predict_many(x)

    def predict_one(self, x: pd.Series) -> bool:
        return self.__model.predict_one(x)
