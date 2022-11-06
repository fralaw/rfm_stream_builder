"""
// Name        : Example.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Classe che modella gli esempi. È formata da una descrizione il quale è lista di Rfm
"""

from Rfm import Rfm


class Example:
    # Attributi privati:
    # __desc; descrizione dell'esempio - lista di oggetti di classe Rfm
    # labelTimeStamp: sarà di tipo datetime e verrà riempita con il momento dell'etichettatura
    __desc: list[Rfm]

    """
        Costruttore: setta il parametro labelTimeStamp e inizializza la lista desc come lista vuota.
    """
    def __init__(self, startTimeStamp):
        self.__startTimeStamp = startTimeStamp
        self.__desc = []

    """
       Metodo che effettua la copia. 
    """
    def copy(self):
        ex = Example(None)
        ex.__desc = self.__desc.copy()
        ex.__startTimeStamp = self.__startTimeStamp
        return ex

    """
        Metodo getter StartTimeStamp.
        Return di un tipo datetime.
    """
    def getStartTimeStamp(self):
        return self.__startTimeStamp

    """
        Metodo add che aggiunge un Rfm alla lista di RFM.
    """
    def addRfm(self, desc: Rfm):
        self.__desc.append(desc)

    """
        Metodo per eliminare l'Rfm in ultima posizione nella lista e inserirne uno passato in input.
    """
    def replaceLastRfm(self, desc: Rfm):
        self.__desc.pop(-1)
        self.__desc.append(desc)

    """
        Metodo getter per desc.
        Return di un tipo lista, la lista di Rfm.
    """
    def getDesc(self):
        return self.__desc
