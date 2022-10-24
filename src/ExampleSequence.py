"""
// Name        : ExampleSequence.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe che modella la sequenza di esempi. E' formata da un unico attributo: la lista di Examples
"""

from Example import Example


class ExampleSequence:
    __examples: list[Example]

    def __init__(self):
        self.__examples = []

    def appendExample(self, ex: Example):
        self.__examples.append(ex)
