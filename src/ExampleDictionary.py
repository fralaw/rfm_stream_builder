"""
// Name        : ExampleDictionary.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe che modella la sequenza di esempi. E' formata da un unico attributo: la lista di ExampleSequence
                 Ogni K_Member di Receipts è chiave nel dizionario dict<k,v> dove v: è di tipo ExampleSequence.
"""

from Example import Example
from ExampleSequence import ExampleSequence


class ExampleDictionary:

    # Metodo costruttore che inizializza un dizionario vuoto
    def __init__(self):
        self.__examples = {}

    # Metodo per restituire il dizionario
    def getDict(self):
        return self.__examples

    # Metodo che verifica l'esistenza della chiave passata come parametro nella lista delle chiavi
    def containsKey(self, customer: str):
        if customer in self.__examples.keys():
            return True
        else:
            return False

    # Metodo per inserire un esempio nell'ExampleSequence all'interno del dizionario con chiave customer
    def insertExample(self, customer: str, ex: Example):
        if customer not in self.__examples:
            exampleSeq = ExampleSequence()
            exampleSeq.appendExample(ex)
            self.__examples[customer] = exampleSeq
        else:
            self.__examples[customer].appendExample(ex)

    # Meotodo per cancellare un item dal dizionario avente in input un customer
    def delete(self, customer: str):
        del self.__examples[customer]

    # Metodo per etichettare l'esempio.
    def recordLabeledExample(self, customer: str, label: bool, date, stream):
        self.__examples[customer].record(label, date, stream, customer)

    # Metodo di override per la stampa
    def __str__(self):
        return str(self.__examples.items())
