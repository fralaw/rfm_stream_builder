"""
// Name        : ExampleSequence.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Classe che modella la sequenza di esempi. È formata da un unico attributo: la lista di Examples
"""

from Example import Example
import datetime as dt
from Rfm import Rfm


class ExampleSequence:
    __examples: list[Example]

    """ 
        Metodo costruttore. Inizializza la lista di esempi come lista vuota.
    """
    def __init__(self):
        self.__examples = []

    """
    Metodo append per inserire nuovi esempi alla lista di esempi.
    """
    def appendExample(self, ex: Example):
        self.__examples.append(ex)

    """
        Metodo record per etichettare e mettere nello stream gli esempi.
    """
    def record(self, label: bool, date, stream, customer):
        examplesList = [[str(ex.getDesc()), date, str(label), customer] for ex in self.__examples]
        stream.writerows(examplesList)
        self.__examples = []
