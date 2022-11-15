"""
// Name        : IncrementalClassifier.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe astratta che implementa l'interfaccia ClassifierInterface.
"""
import abc
import pandas as pd
from river import base

from ClassifierInterface import ClassifierInterface


class IncrementalClassifier(ClassifierInterface):
    def __init__(self):
        self.__model: base.MiniBatchClassifier = base.MiniBatchClassifier()

    def learn(self, x: pd.DataFrame, y: pd.Series):
        # orient="records" genera una lista dove ogni elemento è una riga del DataFrame sotto forma di dizionario
        x = x.apply(pd.to_numeric, downcast='float')
        self.__model.learn_many(x, y)

    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        # orient="records" genera una lista dove ogni elemento è una riga del DataFrame sotto forma di dizionario
        x = x.apply(pd.to_numeric, downcast='float')
        return self.__model.predict_many(x)

    def predict_one(self, x: pd.Series) -> bool:
        return self.__model.predict_one(x)

    @abc.abstractmethod
    def __abstractClass(self):
        pass
    