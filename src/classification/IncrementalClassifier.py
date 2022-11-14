"""
// Name        : IncrementalClassifier.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Classe astratta che implementa l'interfaccia ClassifierInterface.
"""
import abc
import pandas as pd
from river import base
from ClassifierInterface import ClassifierInterface


class IncrementalClassifier(ClassifierInterface):
    __model: base.MiniBatchClassifier

    @abc.abstractmethod
    def __init__(self):
        pass

    def learn(self, x: pd.DataFrame, y: pd.Series):
        self.__model.learn_many(x, y)

    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        return self.__model.predict_many(x)

    def predict_one(self, x: pd.Series) -> bool:
        return self.__model.predict_one(x)

