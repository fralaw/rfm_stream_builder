"""
// Name        : AdaptiveRandomForestClassifier.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe concreta AdaptiveRandomForestClassifier che eredita da StreamClassifier.
"""
from river import ensemble
from StreamClassifier import StreamClassifier


class AdaptiveRandomForestClassifier(StreamClassifier):
    def __init__(self):
        self.__model = ensemble.AdaptiveRandomForestClassifier()

    def __abstractClass(self):
        pass
