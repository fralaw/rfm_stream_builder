"""
// Name        : LogisticRegression.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Classe concreta LogisticRegression che eredita da IncrementalClassifier.
"""
import pandas as pd
from river import linear_model
from IncrementalClassifier import IncrementalClassifier


class LogisticRegression(IncrementalClassifier):
    def __init__(self):
        self.__model = linear_model.LogisticRegression()
