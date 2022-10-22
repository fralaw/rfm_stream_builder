"""
// Name        : Rfm.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : La classe Rfm modella gli attributi Recency, Frequency e Monetary.
                 RFM è un modello utilizzato per analizzare il valore del cliente.
                 Recency: quanto tempo è trascorso dall'ultima attività o transazione;
                 Frequency: con quale frequenza un cliente ha effettuato transazioni o interagito;
                 Monetary: questo fattore riflette quanto un cliente ha speso.
"""

class Rfm:
    # Metodo costruttore
    def __init__(self, recency, frequency, monetary):
        self.__recency = recency
        self.__frequency = frequency
        self.__monetary = monetary

    # Metodo get per Recency
    def getRecency(self):
        return self.__recency

    # Metodo get per Frequency
    def getFrequency(self):
        return self.__frequency

    # Metodo get per Monetary
    def getMonetary(self):
        return self.__monetary

    # Metodo toScore: da rivalutare
    #def toScore(self):