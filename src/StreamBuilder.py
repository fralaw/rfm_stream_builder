"""
// Name        : StreamBuilder.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Classe centrale del nostro progetto. Ha il compito di avviare il ciclo di estrazione dei dati dal db,
                 attraverso l'inizializzazione di una connessione usando la classe DBConnector. Viene successivamente
                 aperto il file csv su cui serializziamo gli esempi.
                 Il metodo privato generateStream genererà esempi opportunamente etichettati.
                 Infine la connessione al db e il file verranno chiuse.
"""

from alive_progress import alive_bar
from collections import deque
import datetime as dt
import pandas as pd
import cProfile
from DBConnector import DBConnector
from DataWindow import DataWindow


class StreamBuilder:
    """
        Metodo costruttore:
            - host: Il nome del server o l'indirizzo IP su cui è in esecuzione MySQL. Se si esegue su localhost,
                    è possibile utilizzare localhost o il suo IP 127.0.0.0;
            - username: Il nome utente che si utilizza per lavorare con MySQL.
                        Il nome utente predefinito per il database MySQL è 'root';
            - password: La password viene fornita dall'utente al momento dell'installazione del server MySQL.
                        Se si usa root, non c'è bisogno della password;
            - databaseName: Il nome del database a cui si desidera connettersi ed eseguire le operazioni.
            - churnDim: dimensione del churn, di tipo int;
            - periodDim: dimensione del periodo, di tipo int;
            - periods: numero di periodi, di tipo int;
            - streamPath: percorso del file dove avverrà la serializzazione;
            - start: data di partenza, di default la prima del db;
            - end: data di fine, di default l'ultima del db;
            - labeledExamples: oggetto pandas in cui inserire gli esempi etichettati.
        Inizializza la DataWindow e richiama il metodo privato generateStream().
    """
    def __init__(self, host: str, username: str, password: str, databaseName: str,
                 churnDim: int, periodDim: int, periods: int, streamPath: str, start: dt.date = None,
                 end: dt.date = None):
        self.__mydb = DBConnector(host, username, password, databaseName)
        self.__window: DataWindow = DataWindow(periodDim, periods, churnDim)
        columns = []
        for i in range(1, periods + 1):
            columns += [f'Recency{i}', f'Frequency{i}', f'Monetary{i}']
        columns += ['Generation Timestamp', 'Label Timestamp', 'Label', 'Customer']
        self.__labeledExamples: pd.DataFrame = pd.DataFrame(columns=columns)
        self.__labeledExamples.to_csv(streamPath, mode='w', index=False)
        self.__generateStream(streamPath, start, end)

    """
        Metodo per la generazione ed etichettatura di esempi. Infine salviamo gli esempi in un file.
    """
    def __generateStream(self, streamPath: str, start: dt.date, end: dt.date):
        currentDay = self.__mydb.extractFirstDay() if start is None else start
        lastDay = self.__mydb.extractLastDay() if end is None else end
        with alive_bar((lastDay-currentDay).days, force_tty=True) as bar:
            while currentDay != lastDay:
                deq = deque()
                dataOfDay = self.__mydb.extractReceipts(currentDay)
                self.__window.deleteFurthestDay()
                self.__window.set(dataOfDay, currentDay)
                self.__window.generateLabels(deq)
                self.__window.generateExamples(deq)
                self.__window.clean()
                self.__labeledExamples = pd.DataFrame(deq, columns=self.__labeledExamples.columns)
                self.__labeledExamples.sort_values(['Label Timestamp'], ascending=True, inplace=True)
                self.__insertLabeledExamples(streamPath)
                self.__labeledExamples = self.__labeledExamples.iloc[0:0]
                currentDay += dt.timedelta(days=1)
                bar()
        self.__mydb.closeConnection()

    def __insertLabeledExamples(self, streamPath):
        self.__labeledExamples.to_csv(streamPath, index=False, mode='a', header=False)


StreamBuilder("localhost", "root", "", "", 3, 2, 2, "stream.csv")
