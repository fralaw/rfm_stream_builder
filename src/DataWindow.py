import csv
import datetime as dt
from itertools import islice
import numpy as np

import pandas as pd

from ExampleSequence import ExampleSequence
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
            receipts.append(Receipt(row[0], row[1], row[2], row[3], row[5], row[4]))
            # T_Receipt
            lastPurchase = row[4]

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
                        cw.setDay(day, lastPurchase, index)
                        self.__window[oldMember] = cw
                    # Svuotiamo la lista di receipts
                    receipts = []
                    # Settiamo il nuovo K_Member come old
                    oldMember = row[1]
                # Aggiungi la ricevuta alla lista di receipts
                receipts.append(Receipt(row[0], row[1], row[2], row[3], row[5], row[4]))
                lastPurchase = row[4]

                # L'ultimo cliente non sarà mai precedente di nessuno, viene aggiunto a prescindere
                if i == len(data) - 1:
                    day = Day(receipts)
                    try:
                        self.__window[row[1]].setDay(day, lastPurchase, index)
                    except KeyError:
                        cw = CustomerWindow(row[1], lastPurchase, self.__dim * self.__periods)
                        self.__window[row[1]] = cw.setDay(day, lastPurchase, index)
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
    def generateExamples(self, index, writer):
        # Calcolo degli indici:
        # currentPeriodIndex = indice del periodo in cui è stato effettuato l'acquisto
        currentPeriodIndex = int(index / self.__dim)
        # currentDayIndex = posizione nel periodo
        currentDayIndex = index - (currentPeriodIndex * self.__dim)

        # CASO 1:
        # Generazione esempi per tutti quei clienti che sono nel dizionario ExampleDictionary in attesa di essere
        # etichettati e non hanno comprato oggi

        # Lista di customer window dei clienti che in current day non hanno effettuato acquisti
        try:
            windows = [cw for cw in self.__window.values()
                       if self.__dim <= self.__currentDay - cw.getLastReceipt() >= 1]
            for cw in windows:
                periods = self.__splitPeriods(cw)
                ex = Example(self.__currentDay)
                for i in range(0, currentPeriodIndex):
                    period = periods[i]
                    # Ci troviamo prima del periodo corrente - calcolare RFM globale delle settimane precedenti.
                    if i != currentPeriodIndex:
                        rfm = self.__calculateRFM(period)
                        ex.addExample(Rfm(rfm[0], rfm[1], rfm[2]))
                    # Altrimenti calcola RFM del current day
                    else:
                        rfm = self.__calculateRFM(period, end=currentDayIndex)
                        ex.addExample(Rfm(rfm[0], rfm[1], rfm[2]))
                # Inserisce nuovo esempio nel dizionario
                self.__examples.insertExample(cw.getKMember(), ex)
        except TypeError:
            pass

            # CASO 2:
            # Generazione esempi per tutti quei clienti che hanno effettuato acquisti nel current day

        try:
            # Lista di customer window dei clienti che in current day hanno effettuato acquisti
            windows = [cw for cw in self.__window.values() if cw.getLastReceipt().date() == self.__currentDay]
            for cw in windows:
                print(cw.getKMember())
                periods = self.__splitPeriods(cw)
                ex = Example(self.__currentDay)
                i = 0
                while i <= currentPeriodIndex:
                    period = periods[i]
                    # Ci troviamo prima del periodo corrente - calcolare RFM globale delle settimane precedenti.
                    if i != currentPeriodIndex:
                        try:
                            rfm = self.__calculateRFM(period)
                        except IndexError:
                            rfm = [0, 0, 0]
                        ex.addExample(Rfm(rfm[0], rfm[1], rfm[2]))
                    # Ci troviamo nel periodo attuale. Calcoliamo RFM considerando il caso vi siano più di una ricevuta
                    # nella stessa giornata. In tal caso costruiamo un ExampleSequence che immagazzina tutti gli esempi
                    # che devono essere etichettati subito dopo la generazione.
                    else:
                        receipt = period[currentDayIndex].getReceiptsOfDay()[0]
                        if len(period[currentDayIndex].getReceiptsOfDay()) > 1:
                            seq = ExampleSequence()
                            exampletoWrite = Example(self.__currentDay)
                            try:
                                rfm = self.__calculateRFM(period, end=currentDayIndex - 1)
                            except IndexError:
                                rfm = [0, 1, receipt.getQAmount()]
                            exampletoWrite.addExample(Rfm(rfm[0], rfm[1], rfm[2]))
                            seq.appendExample(exampletoWrite)
                            for i in range(1, len(period[currentDayIndex].getReceiptsOfDay()) - 2):
                                exampletoWrite = Example(self.__currentDay)
                                receipt = period[currentDayIndex].getReceiptsOfDay()[i]
                                rfm = [0, rfm[1] + 1, rfm[2] + receipt.getQAmount()]
                                exampletoWrite.addExample(Rfm(rfm[0], rfm[1], rfm[2]))
                                seq.appendExample(exampletoWrite)
                            seq.record(False, self.__currentDay, writer)
                        # Infine generiamo l'esempio per l'ultimo acquisto che va nel dizionario ExampleDictionary
                        try:
                            rfm = self.__calculateRFM(period, end=currentDayIndex)
                        except IndexError:
                            rfm = [0, 1, receipt.getQAmount()]
                        ex.addExample(Rfm(rfm[0], rfm[1], rfm[2]))
                    i = i + 1
                self.__examples.insertExample(cw.getKMember(), ex)
        except TypeError:
            pass

    def __splitPeriods(self, cw: CustomerWindow):
        days = cw.getListOfDays()
        iter_days = iter(days)
        length_to_split = [self.__dim] * self.__periods
        # Dividiamo la window in periodi
        return [list(islice(iter_days, elem)) for elem in length_to_split]

    def __calculateRFM(self, period: list[Day], start=0, end=__dim - 1):
        if end not in range(0, self.__dim - 1):
            raise IndexError
        recency = 0
        frequency = 0
        monetary = 0
        i = start
        while i <= end:
            try:
                receipts = period[i].getReceiptsOfDay()
                recency = end - i
                frequency += len(receipts)
                monetary += np.sum([receipt.getQAmount() for receipt in receipts])
            except AttributeError:
                pass
            i += 1
        return [recency, frequency, monetary]


"""
 iter_days = iter(days)
            length_to_split = [self.__dim] * self.__periods
            periods = [list(islice(iter_days, elem))
                       for elem in length_to_split]"""
