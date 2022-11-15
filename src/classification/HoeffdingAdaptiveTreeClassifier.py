"""
// Name        : HoeffdingAdaptiveTreeClassifier.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe concreta HoeffdingAdaptiveTreeClassifier che eredita da StreamClassifier.
"""
from river import tree
from StreamClassifier import StreamClassifier


class HoeffdingAdaptiveTreeClassifier(StreamClassifier):
    def __init__(self):
        self.__model = tree.HoeffdingAdaptiveTreeClassifier()

    def __abstractClass(self):
        pass
