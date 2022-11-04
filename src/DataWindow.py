import csv
import datetime as dt
from itertools import islice
import numpy as np

import pandas as pd
import operator
from RfmException import EmptyRfmException
from ExampleSequence import ExampleSequence
from CustomerWindow import CustomerWindow
from DBConnector import DBConnector
from Day import Day
from Example import Example
from ExampleDictionary import ExampleDictionary
from Receipt import Receipt
from Rfm import Rfm


class DataWindow:
    def __init__(self, periodDim: int, periods: int, churnDim: int):
        self.__churnDim = churnDim
        self.__periodDim: int = periodDim
        self.__periods: int = periods
        self.__windowDim: int = max(periodDim * periods, churnDim)
        self.__currentDay: dt.date = None
        self.__examples: ExampleDictionary = ExampleDictionary()
        self.__window: dict = {}

    def set(self, data: list[tuple], dateToSet: dt.date):
        self.__currentDay = dateToSet
        # Lista che contiene le liste di ricevute di ciascun cliente
        receipts = []
        try:
            # Salviamo il 'K_Member' della lista data in prima posizione, in modo da usarlo come confronto iniziale
            oldMember = data[0][1]

            # Scandisce la lista di tuple
            for row in data:
                # Confronta l'attuale 'K_Member' con l'old_Member, cioè se siamo ancora sulle ricevute di old cliente
                if row[1] != oldMember:
                    # Costruisce il Day passando come oggetto la lista di receipts
                    day = Day(receipts)
                    try:
                        # Prova ad accedere alla customer window e settare il day in posizione index
                        self.__window[oldMember].setDay(day, lastPurchase)
                    except KeyError:
                        # Altrimenti inizializza
                        cw = CustomerWindow(oldMember, self.__windowDim)
                        cw.setDay(day, lastPurchase)
                        self.__window[oldMember] = cw
                    # Svuotiamo la lista di receipts
                    receipts = [
                        Receipt(row[0], row[1], row[2], row[3], row[4], row[5])
                    ]
                    lastPurchase = row[5]
                    # Settiamo il nuovo K_Member come old
                    oldMember = row[1]
                else:
                    receipts.append(Receipt(row[0], row[1], row[2], row[3], row[4], row[5]))
                    lastPurchase = row[5]
            # L'ultimo cliente non sarà mai precedente di nessuno, viene aggiunto a prescindere
            day = Day(receipts)
            try:
                self.__window[row[1]].setDay(day, lastPurchase)
            except KeyError:
                cw = CustomerWindow(row[1], self.__windowDim)
                cw.setDay(day, lastPurchase)
                self.__window[row[1]] = cw
        except IndexError:
            pass

    def clean(self):
        self.__window = {key: value for (key, value) in self.__window.items() if not value.isEmpty()}

    def deleteFurthestDay(self):
        for val in self.__window.values():
            val.deleteFurthestDay()

    # Generazione di un esempio per ogni ricevuta del giorno attuale. Generazione dell'esempio anche per i giorni in cui
    # non ha ricevute ma ha un esempio nel dict in attesa di etichettatura.
    # Per ogni esempio calcolo RFM sui giorni precedenti al currentDay divisi per periodo.
    def generateExamples(self, writer):
        # CASO 1:
        # Generazione esempi per tutti quei clienti che sono nel dizionario ExampleDictionary in attesa di essere
        # etichettati e non hanno comprato oggi

        try:
            # Lista di customer window dei clienti che in current day non hanno effettuato acquisti
            windows = [cw for cw in self.__window.values()
                       if 1 <= (self.__currentDay - cw.getLastReceipt().date()).days < self.__churnDim]
            for cw in windows:
                periods = self.__splitPeriods(cw)
                ex = Example(self.__currentDay)
                for period in periods:
                    rfm = self.__calculateRFM(period)
                    ex.addRfm(rfm)
                # Inserisce l' esempio nel dizionario. Esso è formato dai k (con k==periods) RFM calcolati.
                self.__examples.insertExample(cw.getKMember(), ex)
        except TypeError:
            pass

        # CASO 2:
        # Generazione esempi per tutti quei clienti che hanno effettuato acquisti nel current day
        try:
            # Lista di customer window dei clienti che in current day hanno effettuato acquisti
            windows = [cw for cw in self.__window.values() if cw.getLastReceipt().date() == self.__currentDay]
            for cw in windows:
                rfm = Rfm()
                periods = self.__splitPeriods(cw)
                ex = Example(self.__currentDay)
                for period in periods:
                    rfm = self.__calculateRFM(period)
                    # Aggiunge Rfm all'esempio
                    ex.addRfm(rfm)
                self.__examples.insertExample(cw.getKMember(), ex)
                day = operator.itemgetter(-1)(cw.getListOfDays())
                receipts = day.getReceiptsOfDay()
                # Se in un Day ci sono più ricevute
                if len(receipts) > 1:
                    seq = ExampleSequence()
                    for receipt in receipts.reverse()[0:len(receipts) - 1]:
                        rfm = Rfm(rfm.getRecency(), rfm.getFrequency()-1, rfm.getMonetary() - receipt.getQAmount())
                        ex.replaceLastRfm(rfm)
                        seq.appendExample(ex)
        except TypeError:
            pass

    def __splitPeriods(self, cw: CustomerWindow):
        days = cw.getListOfDays()
        iter_days = iter(days)
        length_to_split = [self.__periodDim] * self.__periods
        # Dividiamo la window in periodi
        return [list(islice(iter_days, elem)) for elem in length_to_split]

    def __calculateRFM(self, period: list[Day]):
        recency = 0
        frequency = 0
        monetary = 0
        for day in period:
            try:
                receipts = day.getReceiptsOfDay()
                recency = self.__periodDim - period.index(day)
                frequency += len(receipts)
                monetary += np.sum([receipt.getQAmount() for receipt in receipts])
            except AttributeError:
                pass
        return Rfm(recency, frequency, monetary)

    def generateLabels(self, stream):
        try:
            windows = [cw for cw in self.__window.values() if cw.getLastReceipt().date() == self.__currentDay]
            for cw in windows:
                try:
                    self.__examples.recordLabeledExample(cw.getKMember(), False, self.__currentDay, stream)
                    self.__examples.delete(cw.getKMember())
                except KeyError:
                    pass
        except TypeError:
            pass

        try:
            windows = [cw for cw in self.__window.values() if
                       (self.__currentDay - cw.getLastReceipt().date()).days == self.__churnDim]
            for cw in windows:
                try:
                    self.__examples.recordLabeledExample(cw.getKMember(), True, self.__currentDay, stream)
                    self.__examples.delete(cw.getKMember())
                except KeyError:
                    pass
        except TypeError:
            pass
