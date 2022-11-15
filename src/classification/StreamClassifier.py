"""
// Name        : StreamClassifier.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe astratta che implementa l'interfaccia ClassifierInterface.
"""

import abc
import pandas as pd
from river import base
from ClassifierInterface import ClassifierInterface


class StreamClassifier(ClassifierInterface):

    @abc.abstractmethod
    def __init__(self):
        __model: base.Classifier = base.Classifier()

    def learn(self, x: pd.DataFrame, y: pd.Series):
        # orient="records" genera una lista dove ogni elemento è una riga del DataFrame sotto forma di dizionario
        x_dict = x.to_dict(orient="records")
        for x_row, y_row in zip(x_dict, y):
            self.__model.learn_one(x_row, y_row)

    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        # orient="records" genera una lista dove ogni elemento è una riga del DataFrame sotto forma di dizionario
        x_dict = x.to_dict(orient="records")
        labels = []
        for row in x_dict:
            label = self.__model.predict_one(row)
            labels.append(label)
        return pd.Series(labels)

    def predict_one(self, x: pd.Series) -> bool:
        return self.__model.predict_one(x.to_dict())

    @abc.abstractmethod
    def __abstractClass(self):
        pass
