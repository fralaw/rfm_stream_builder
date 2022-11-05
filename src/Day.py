"""
// Name        : Day.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : La classe Day modella l'insieme di ricevute di un dato cliente raccolte in una specifica giornata.
                 Un Day è dunque una collezione di Receipts.
"""

from Receipt import Receipt


class Day:
    __receipts: list[Receipt] = []

    """ 
        Metodo costruttore. Riceve in input un parametro opzionale, ovvero la lista di receipts.
        Di default viene inizializzata a lista vuota. 
        Se viene passata una lista si effettua una copia dell'oggetto tramite il .copy().
    """
    def __init__(self, receipts: list = None):
        if receipts is None:
            self.__receipts = []
        if type(receipts) is list:
            self.__receipts = receipts.copy()
        else:
            raise TypeError

    """
        Metodo per aggiungere una nuova receipt alla lista.
    """
    def addReceipt(self, receipt: Receipt):
        self.__receipts.append(receipt)

    """
        Metodo getter per receipts
        Return di un tipo lista di Receipt.
    """
    def getReceiptsOfDay(self):
        return self.__receipts

    """
        Override del metodo __str__.
        Return di un tipo string
    """
    def __str__(self):
        receiptsToStr = str()
        for r in self.__receipts:
            receiptsToStr += (str(r) + "\n\n")
        return receiptsToStr
