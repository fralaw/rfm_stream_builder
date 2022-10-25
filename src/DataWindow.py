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

    def __init__(self, dim: int, periods: int):
        self.__dim: int = dim
        self.__periods: int = periods
        self.__currentDay: dt.date = None
        self.__examples: ExampleDictionary = ExampleDictionary()
        self.__window: dict = {}

    def set(self, data: pd.DataFrame, index: int | None = None):
        if index is None:
            index = (self.__dim * self.__periods) - 1
        self.__currentDay = data.iloc[0]["T_Receipt"].to_pydatetime().date()
        receipts = []
        for i in range(0, data.shape[0] - 1):

            row = data.iloc[i]
            K_Receipt = row["K_Receipt"]
            K_Member = row["K_Member"]
            Quantity = row["Quantity"]
            Q_Amount = row["Q_Amount"]
            Q_Discount_Amount = row["Q_Discount_Amount"]
            T_Receipt = row["T_Receipt"].to_pydatetime()

            receipts.append(
                Receipt(K_Receipt, K_Member, Quantity, Q_Amount, Q_Discount_Amount, T_Receipt))
            lastPurchase = T_Receipt

            if data.iloc[i + 1]["K_Member"] != K_Member:
                day = Day(receipts)
                if K_Member not in self.__window:
                    cw = CustomerWindow(K_Member, self.__dim * self.__periods)
                    cw.setDay(day, lastPurchase, index)
                    self.__window[K_Member] = cw
                else:
                    self.__window[K_Member].setDay(day, lastPurchase, index)
                receipts.clear()

        row = data.iloc[data.shape[0] - 1]
        K_Receipt = row["K_Receipt"]
        K_Member = row["K_Member"]
        Quantity = row["Quantity"]
        Q_Amount = row["Q_Amount"]
        Q_Discount_Amount = row["Q_Discount_Amount"]
        T_Receipt = row["T_Receipt"].to_pydatetime()

        receipts.append(
            Receipt(K_Receipt, K_Member, Quantity, Q_Amount, Q_Discount_Amount, T_Receipt))
        lastPurchase = T_Receipt
        day = Day(receipts.copy())
        if K_Member not in self.__window:
            cw = CustomerWindow(K_Member, self.__dim * self.__periods)
            cw.setDay(day, lastPurchase, index)
            self.__window[K_Member] = cw
        else:
            self.__window[K_Member].setDay(day, lastPurchase, index)
        receipts.clear()

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
                            self.__examples.insertExample(elem[0], example)
                    else:
                        recency = len(period) - period.index(day) - 1
                        rfm = Rfm(recency, frequency, monetary)
                        example.addExample(rfm)
                        self.__examples.insertExample(elem[0], example)




dw = DataWindow(7, 4)
db = DBConnector(password="Cicciopazzo98")
df = db.extractReceipts(dt.date(2009, 1, 12))
dw.set(df, 1)
dw.set(df, 15)

dw.generateExamples()
