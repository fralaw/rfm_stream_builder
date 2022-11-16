"""
// Name        : OnlineLearner.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 2.0
// Description : Classe OnlineLearner.
"""

import pandas as pd

from AdaptiveRandomForestClassifier import AdaptiveRandomForestClassifier
from HoeffdingAdaptiveTreeClassifier import HoeffdingAdaptiveTreeClassifier
from Perceptron import Perceptron
from LogisticRegression import LogisticRegression
from PickleLoader import PickleLoader


class OnlineLearner:
    def __init__(self, classifierName: str, fromPickle: str = None):
        self.__classifierName = classifierName
        match classifierName:
            case 'AdaptiveRandomForestClassifier':
                self.__model = AdaptiveRandomForestClassifier()
            case 'HoeffdingAdaptiveTreeClassifier':
                self.__model = HoeffdingAdaptiveTreeClassifier()
            case 'Perceptron':
                self.__model = Perceptron()
            case 'LogisticRegression':
                self.__model = LogisticRegression()
            case _:
                pass

    def train(self, loader: PickleLoader):
        for df in loader:
            X = df.iloc[:, 0:-1]
            y = df.iloc[:, -1]
            self.__model = self.__model.learn(X, y)

    def predict(self, loader: PickleLoader):
        labels = pd.Series()
        for df in loader:
            X = df.iloc[:, 0:-1]
            pd.concat(labels, self.__model.predict_many(X))
        return labels

    def test(self, loader: PickleLoader):
        predicted_labels = []
        true_labels = []
        for df in loader:
            X = df.iloc[:, 0:-1]
            true_labels += list(df.iloc[:, -1])
            predicted_labels += list(self.__model.predict_many(X))
        target = pd.Series(predicted_labels)
        y_test = pd.Series(true_labels)
        df = pd.concat([y_test, target], axis=1)
        return df

    def toPickle(self, folderPath: str):
        pass
