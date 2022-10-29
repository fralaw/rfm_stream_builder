import csv
import datetime as dt
from itertools import islice
import numpy as np

import pandas as pd

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
                        cw.setDay(day, lastPurchase, index)
                        self.__window[oldMember] = cw
                    # Svuotiamo la lista di receipts
                    receipts = []
                    # Settiamo il nuovo K_Member come old
                    oldMember = row[1]
                # Aggiungi la ricevuta alla lista di receipts
                receipts.append(Receipt(row[0], row[1], row[2], row[3], row[4], row[5]))
                lastPurchase = row[5]

                # L'ultimo cliente non sarà mai precedente di nessuno, viene aggiunto a prescindere

            day = Day(receipts)
            try:
                self.__window[row[1]].setDay(day, lastPurchase, index)
            except KeyError:
                cw = CustomerWindow(row[1], (self.__dim * self.__periods))
                cw.setDay(day, lastPurchase, index)
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
    def generateExamples(self, index, writer):
        # Calcolo degli indici:
        # currentPeriodIndex = indice del periodo in cui è stato effettuato l'acquisto
        currentPeriodIndex = int(index / self.__dim)
        # currentDayIndex = posizione nel periodo
        currentDayIndex = index - (currentPeriodIndex * self.__dim)

        # [],[r1],[],[],[],[],[]     |     [],[],[churn],[],[],[],[r5]     |      [],[],[],[r2],[],[],[]     |      [],[],[],[],[],[],[]
        # CASO 1:
        # Generazione esempi per tutti quei clienti che sono nel dizionario ExampleDictionary in attesa di essere
        # etichettati e non hanno comprato oggi

        # Lista di customer window dei clienti che in current day non hanno effettuato acquisti
        try:
            windows = [cw for cw in self.__window.values()
                       if 1 <= self.__currentDay - cw.getLastReceipt().date() <= self.__dim]
            for cw in windows:
                periods = self.__splitPeriods(cw)
                ex = Example(self.__currentDay)
                i = 0
                while i <= currentPeriodIndex:
                    period = periods[i]
                    # Ci troviamo prima del periodo corrente - calcolare RFM globale delle settimane precedenti.
                    if i != currentPeriodIndex:
                        # Prova a calcolare RFM GLOBALE per la settimana precedente
                        try:
                            rfm = self.__calculateRFM(period)
                        # Caso in cui la settimana prima ha tutti i day vuoti (no ricevute).
                        except EmptyRfmException:
                            # Settiamo un RFM a 0. La Recency sarà massima.
                            rfm = (Rfm(self.__dim, 0, 0))
                        # Aggiunge rfm all'esempio
                        ex.addRfm()
                    # Altrimenti calcola RFM relativo al current day
                    else:
                        # Prova a calcolare RFM fino al currentDay all'interno del periodo corrente i=currentPeriodIndex
                        try:
                            rfm = self.__calculateRFM(period, end=currentDayIndex)
                        # Caso in cui non ci sono acquisti. Genera RFM a 0. La Recency sarà comunque corretta.
                        except EmptyRfmException:
                            rfm = Rfm(self.__currentDay - cw.getLastReceipt().date(), 0, 0)
                        ex.addRfm(rfm)
                    i += 1
                # Inserisce l' esempio nel dizionario. Esso è formato dai k (con k<=periods) RFM calcolati.
                self.__examples.insertExample(cw.getKMember(), ex)
        except TypeError:
            pass

        # CASO 2:
        # Generazione esempi per tutti quei clienti che hanno effettuato acquisti nel current day
        # [],[],[],[],[],[],[]     |     [],[],[],[],[],[],[]     |      [],[],[r6],[r2,r3,r4,r5],[],[],[]     |      [],[],[],[],[],[],[]

        try:
            # Lista di customer window dei clienti che in current day hanno effettuato acquisti
            windows = [cw for cw in self.__window.values() if cw.getLastReceipt().date() == self.__currentDay]
            for cw in windows:
                periods = self.__splitPeriods(cw)
                ex = Example(self.__currentDay)
                # i = currentPeriodIndex se prima del giorno attuale il cliente non ha effettuato acquisti.
                # 0 (primo periodo) altrimenti
                flag = True
                i = 0
                while flag and i < currentPeriodIndex:
                    period = periods[i]
                    if period == [None]*self.__dim:
                        flag = False
                    i += 1
                while i <= currentPeriodIndex:
                    period = periods[i]
                    # Ci troviamo prima del periodo corrente - calcolare RFM globale delle settimane precedenti.
                    if i != currentPeriodIndex:
                        try:
                            rfm = self.__calculateRFM(period)
                        except EmptyRfmException:
                            # Settiamo un RFM a 0. La Recency sarà massima.
                            rfm = (Rfm(self.__dim, 0, 0))
                        # Aggiunge Rfm all'esempio
                        ex.addRfm(rfm)

                    # Ci troviamo nel periodo attuale. Calcoliamo RFM considerando il caso vi siano più di una ricevuta
                    # nella stessa giornata. In tal caso costruiamo un ExampleSequence che immagazzina tutti gli esempi
                    # che devono essere etichettati subito dopo la generazione.
                    else:
                        # Prova a calcolare RFM fino al giorno prima del currentDay all'interno del periodo corrente
                        # i=currentPeriodIndex
                        try:
                            rfm = self.__calculateRFM(period, end=currentDayIndex - 1)
                        # Caso in cui non ci sono acquisti. Genera RFM a 0. La Recency sarà comunque corretta.
                        except EmptyRfmException:
                            rfm = Rfm((self.__currentDay - cw.getLastReceipt().date()).days, 0, 0)

                        receipts = period[currentDayIndex].getReceiptsOfDay()
                        newRfm = Rfm(rfm.getRecency() + 1, rfm.getFrequency() + 1,
                                  rfm.getMonetary() + receipts[0].getQAmount())
                        rfm = newRfm
                        if len(receipts) > 1:
                            seq = ExampleSequence()
                            toWrite = ex.copy()
                            toWrite.addRfm(rfm)
                            seq.appendExample(toWrite)
                            for receipt in [receipt for receipt in receipts[1: -1]]:
                                rfm = Rfm(0, rfm.getFrequency() + 1, rfm.getMonetary() + receipt.getQAmount())
                                toWrite = ex.copy()
                                toWrite.addRfm(rfm)
                                seq.appendExample(toWrite)
                            seq.record(False, self.__currentDay, writer)
                        else:
                            ex.addRfm(rfm)
                    i += 1
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
        if frequency == 0:
            raise EmptyRfmException
        return Rfm(recency, frequency, monetary)
