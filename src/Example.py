"""
// Name        : Example.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe che modella gli esempi. E' formata da una descrizione il quale è lista di Rfm
"""

from Rfm import Rfm


class Example:
    __desc: list[Rfm] = []
    __labelTimeStamp = None

    def __init__(self, startTimeStamp):
        self.__startTimeStamp = startTimeStamp

    def getStartTimeStamp(self):
        return self.__startTimeStamp

    def addExample(self, desc: Rfm):
        self.__desc.append(desc)

    def getDesc(self):
        return self.__desc

    def setLabelTimeStamp(self, labelTimeStamp):
        self.__labelTimeStamp = labelTimeStamp

    def getLabelTimeStamp(self):
        return self.__labelTimeStamp
