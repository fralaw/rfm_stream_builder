"""
// Name        : Perceptron.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Classe concreta Perceptron che eredita da IncrementalClassifier.
"""
from river import linear_model
from IncrementalClassifier import IncrementalClassifier


class Perceptron(IncrementalClassifier):
    def __init__(self):
        self.__model = linear_model.Perceptron()
