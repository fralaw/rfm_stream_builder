"""
// Name        : Example.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe che modella gli esempi. E' formata da una descrizione il quale è lista di Rfm
"""

from Rfm import Rfm


class Example:
    __desc: list[Rfm] = []

    def __init__(self, startTimeStamp):
        self.__startTimeStamp = startTimeStamp

    def getStartTimeStamp(self):
        return self.__startTimeStamp

    def addExample(self, desc):
        self.__desc.append(desc)

    def getDesc(self):
        return self.__desc
