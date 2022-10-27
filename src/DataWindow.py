import csv
import datetime as dt
from itertools import islice

import pandas as pd

from CustomerWindow import CustomerWindow
from DBConnector import DBConnector
from Day import Day
from Example import Example
from ExampleDictionary import ExampleDictionary
from Receipt import Receipt
from Rfm import Rfm


class DataWindow:
    __dim: int = 0
    __periods: int = 0

    def __init__(self, dim: int, periods: int):
        self.__dim: int = dim
        self.__periods: int = periods
        self.__currentDay: dt.date = None
        self.__examples: ExampleDictionary = ExampleDictionary()
        self.__window: dict = {}

    def set(self, data: list[tuple], dateToSet: dt.date, index: int = (__dim * __periods) - 1):
        self.__currentDay = dateToSet
        # Lista che contiene le liste di ricevute di ciascun cliente
        receipts = []
        try:
            # Prima ricevuta
            row = data[0]
            # Salviamo il 'K_Member' della lista data in prima posizione, in modo da usarlo come confronto iniziale
            oldMember = data[0][1]
            # Aggiungiamo l'oggetto Receipt alla lista.
            receipts.append(Receipt(row[0], row[1], row[2], row[3], row[4], row[5]))
            # T_Receipt
            lastPurchase = row[5]

            # Scandisce la lista di tuple
            for i in range(1, len(data) - 1):
                row = data[i]
                # Confronta l'attuale 'K_Member' con l'old_Member, cioè se siamo ancora sulle ricevute di old cliente
                if row[1] != oldMember:
                    # Costruisce il Day passando come oggetto la lista di receipts
                    day = Day(receipts)
                    try:
                        # Prova ad accedere alla customer window e settare il day in posizione index
                        self.__window[oldMember].setDay(day, lastPurchase, index)
                    except KeyError:
                        # Altrimenti inizializza
                        cw = CustomerWindow(oldMember, self.__dim * self.__periods)
                        self.__window[oldMember] = cw.setDay(day, lastPurchase, index)
                    # Svuotiamo la lista di receipts
                    receipts = []
                    # Settiamo il nuovo K_Member come old
                    oldMember = row[1]
                # Aggiungi la ricevuta alla lista di receipts
                receipts.append(Receipt(row[0], row[1], row[2], row[3], row[4], row[5]))

                # L'ultimo cliente non sarà mai precedente di nessuno, viene aggiunto a prescindere
                if i == len(data-1):
                    day = Day(receipts)
                    try:
                        self.__window[row[1]].setDay(day, lastPurchase, index)
                    except KeyError:
                        cw = CustomerWindow(row[1], self.__dim * self.__periods)
                        self.__window[row[1]] = cw.setDay(day, lastPurchase, index)
        except IndexError:
            pass

    def clean(self):
        for elem in self.__window.items():
            if elem[1].isEmpty():
                del self.__window[elem[0]]

    def deleteLatestDay(self):
        for elem in self.__window.items():
            elem[1].deleteLatestDay()

    def generateExamples(self):
        for elem in self.__window.items():
            example = Example(self.__currentDay)
            days = elem[1].getListOfDays()
            iter_days = iter(days)
            length_to_split = [self.__dim] * self.__periods
            periods = [list(islice(iter_days, elem))
                       for elem in length_to_split]
            for period in periods:
                recency = 0
                frequency = 0
                monetary = 0
                for day in period:
                    if day is not None:
                        for receipt in day.getReceiptsOfDay():
                            recency = len(period) - period.index(day) - 1
                            frequency += 1
                            monetary += receipt.getQAmount()
                            rfm = Rfm(recency, frequency, monetary)
                            example.addExample(rfm)
                    else:
                        recency = len(period) - period.index(day) - 1
                        if monetary != 0:
                            rfm = Rfm(recency, frequency, monetary)
                            example.addExample(rfm)
            self.__examples.insertExample(elem[0], example)

    def generateLabels(self, data: pd.DataFrame, writer):
        for elem in self.__examples.getDict().items():
            timedelta = self.__currentDay - self.__window[elem[0]].getLastReceipt().date()
            if timedelta.days > self.__dim:
                self.__examples.recordLabeledExample(elem[0], True, self.__currentDay, writer)
        if data is not None:
            membersOfDay = data["K_Member"]
            for i in range(0, len(membersOfDay) - 1):
                member = membersOfDay[i]
                self.__examples.recordLabeledExample(member, False, self.__currentDay, writer)
