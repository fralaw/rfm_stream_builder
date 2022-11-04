import csv
import datetime as dt

from DBConnector import DBConnector
from DataWindow import DataWindow


class StreamBuilder:

    def __init__(self, host: str, username: str, password: str, databaseName: str,
                 churnDim: int, periodDim: int, periods: int, streamPath: str, start: dt.date = None,
                 end: dt.date = None):
        self.__mydb = DBConnector(host, username, password, databaseName)
        self.__window: DataWindow = DataWindow(periodDim, periods, churnDim)
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

        file = open(streamPath, "w", newline="")
        stream = csv.writer(file)

        while currentDay != lastDay:
            print(currentDay, lastDay)
            dataOfDay = self.__mydb.extractReceipts(currentDay)
            self.__window.deleteFurthestDay()
            self.__window.set(dataOfDay, currentDay)
            self.__window.clean()
            # self.__window.generateLabels(stream)
            # self.__window.generateExamples(stream)
            currentDay += dt.timedelta(days=1)


StreamBuilder("localhost", "root", "", "test_db", 115, 30, 3, "stream.csv")
