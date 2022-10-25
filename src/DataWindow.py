import datetime as dt

import pandas as pd

from CustomerWindow import CustomerWindow
from DBConnector import DBConnector
from Day import Day
from Receipt import Receipt


class DataWindow:
    __dim = int()
    __periods = int()

    def __init__(self, dim: int, periods: int):
        self.__dim = dim
        self.__periods = periods
        self.__currentDay: dt.date = None
        self.__window: dict = {}

    def set(self, data: pd.DataFrame, index: int = __dim * __periods):
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

        row = data.iloc[data.shape[0]-1]
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
            elem[0].deleteLatestDay()


        



dw = DataWindow(7, 4)
db = DBConnector(password="Cicciopazzo98")
df = db.extractReceipts(dt.date(2009, 1, 12))
print(df.tail(2))
dw.set(df, 1)
