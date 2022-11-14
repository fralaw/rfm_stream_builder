"""
// Name        : StreamClassifier.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Classe astratta che implementa l'interfaccia ClassifierInterface.
"""
import abc
import pandas as pd
from river import base
from ClassifierInterface import ClassifierInterface


class StreamClassifier(ClassifierInterface):
    __model: base.Classifier

    @abc.abstractmethod
    def __init__(self):
        pass

    def learn(self, x: pd.DataFrame, y: pd.Series):
        for index, row in x.iterrows():
            x_row = row.to_dict()
            y_row = y[index]
            self.__model.learn_one(x_row, y_row)

    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        labels = []
        for index, row in x.iterrows():
            x_row = row.to_dict()
            label = self.__model.predict_one(x_row)
            labels.append(label)
        return pd.Series(labels)

    def predict_one(self, x: pd.Series) -> bool:
        return self.__model.predict_one(x.to_dict())
