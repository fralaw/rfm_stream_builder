"""
// Name        : Example.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Classe che modella gli esempi. È formata da una descrizione il quale è lista di Rfm
"""

from Rfm import Rfm
import operator


class Example:
    # Attributi privati:
    # __desc; descrizione dell'esempio - lista di oggetti di classe Rfm
    # labelTimeStamp: sarà di tipo datetime e verrà riempita con il mopmento dell'etichettatura
    __desc: list[Rfm]
    __labelTimeStamp = None

    # Costruttore: setta il parametro labelTimeStamp e inizializza la lista desc come lista vuota
    def __init__(self, startTimeStamp):
        self.__startTimeStamp = startTimeStamp
        self.__desc = []

    def copy(self):
        ex = Example(None)
        ex.__desc = self.__desc.copy()
        ex.__startTimeStamp = self.__startTimeStamp
        return ex

    # Metodo get per StartTimeStamp
    def getStartTimeStamp(self):
        return self.__startTimeStamp

    # Metodo add che "appende" un Rfm alla lista di RFM
    def addRfm(self, desc: Rfm):
        self.__desc.append(desc)

    def replaceLastRfm(self, desc: Rfm):
        self.__desc.pop(-1)
        self.__desc.append(desc)

    # Metodo get per ritornare la lista di Rfm
    def getDesc(self):
        return self.__desc

    # Metodo set per labelTimeStamp
    def setLabelTimeStamp(self, labelTimeStamp):
        self.__labelTimeStamp = labelTimeStamp

    # Metodo get per labelTimeStamp
    def getLabelTimeStamp(self):
        return self.__labelTimeStamp
