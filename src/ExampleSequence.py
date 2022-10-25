"""
// Name        : ExampleSequence.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe che modella la sequenza di esempi. E' formata da un unico attributo: la lista di Examples
"""

from Example import Example
from Rfm import Rfm
import csv


class ExampleSequence:
    __examples: list[Example]

    # Costruttore: inizializza la lista example come lista vuota
    def __init__(self):
        self.__examples = []

    # Metodo append per aggiungere un nuovo esempio alla sequenza di esempi
    def appendExample(self, ex: Example):
        self.__examples.append(ex)

    def record(self, label: bool, date, stream):
        for ex in self.__examples:
            description = ex.getDesc()
            ex.setLabelTimeStamp(date)
            for rfm in description:
                row = str(rfm) + "," + str(ex.getLabelTimeStamp()) + "," + str(label)
                stream.writerow(row)
