"""
// Name        : ExampleSequence.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe che modella la sequenza di esempi. E' formata da un unico attributo: la lista di Examples
"""
import csv

from Example import Example
import datetime as dt
from Rfm import Rfm


class ExampleSequence:
    __examples: list[Example]

    # Costruttore: inizializza la lista example come lista vuota
    def __init__(self):
        self.__examples = []

    # Metodo append per aggiungere un nuovo esempio alla sequenza di esempi
    def appendExample(self, ex: Example):
        self.__examples.append(ex)

    # Metodo record per etichettare e inserire nello stream.
    def record(self, label: bool, date, stream):
        examplesList = [[str(ex.getDesc()), date, str(label)] for ex in self.__examples]
        stream.writerows(examplesList)
        self.__examples = []
