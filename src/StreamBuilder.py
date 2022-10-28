import csv
import datetime as dt

from DBConnector import DBConnector
from DataWindow import DataWindow


class StreamBuilder:

    def __init__(self, host: str, username: str, password: str, databaseName: str,
                 churnDim: int, periods: int, streamPath: str, start: dt.date = None, end: dt.date = None):
        self.__mydb = DBConnector(host, username, password, databaseName)
        self.__window: DataWindow = DataWindow(churnDim, periods)
        self.__generateStream(streamPath, start, end, churnDim, periods)

    def __generateStream(self, streamPath: str, start: dt.date, end: dt.date, churnDim: int, periods: int):
        currentDay = dt.date.today()
        if start is None:
            currentDay = self.__mydb.extractFirstDay()
        else:
            currentDay = start

        lastDay = dt.date.today()
        if end is None:
            lastDay = self.__mydb.extractLastDay()
        else:
            lastDay = end

        file = open(streamPath, "w")
        stream = csv.writer(file)
        lastPosition = (churnDim * periods) - 1
        pos = 0
        while currentDay != lastDay:
            dataOfDay = self.__mydb.extractReceipts(currentDay)
            if pos != lastPosition:
                self.__window.set(dataOfDay, currentDay, pos)
            else:
                self.__window.deleteFurthestDay()
                self.__window.set(dataOfDay, currentDay)
                self.__window.clean()
            self.__window.generateExamples(pos, stream)
            # self.__window.generateLabels(dataOfDay, stream)
            currentDay += dt.timedelta(days=1)
            print(currentDay, lastDay)
            pos += 1


StreamBuilder("localhost", "root", "Cicciopazzo98", "churn_retail_db", 7, 4, "stream.csv", start=dt.date(2010, 4, 1))
