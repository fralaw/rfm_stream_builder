"""
// Name        : LogisticRegression.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe concreta LogisticRegression che eredita da IncrementalClassifier.
"""
from river import linear_model
from IncrementalClassifier import IncrementalClassifier


class LogisticRegression(IncrementalClassifier):

    def __init__(self):
        self.__model = linear_model.LogisticRegression()

    def __abstractClass(self):
        pass
