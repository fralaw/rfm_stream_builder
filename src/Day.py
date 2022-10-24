from Receipt import Receipt

"""
// Name        : Day.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : La classe Day modella l'insieme di ricevute di un dato cliente raccolte in una specifica giornata.
Possiede un metodo costruttore con argomento opzionale, un metodo di set (addReceipt) e un metodo di get
"""


class Day:
    # Converrebbe aggiungere attributo timestamp?
    __receipts: list[Receipt] = []

    # Metodo costruttore
    def __init__(self, receipts: list = None):
        if receipts is None:
            receipts = []
        if receipts is not None:
            for r in receipts:
                self.__receipts.append(r)

    # Metodo set
    def addReceipt(self, receipt: Receipt):
        self.__receipts.append(receipt)

    # Metodo get
    def getReceiptsOfDay(self):
        return self.__receipts

    # Metodo di override per la stampa
    def __str__(self):
        receiptsToStr = str()
        for r in self.__receipts:
            receiptsToStr += (str(r) + "\n\n")
        return receiptsToStr
