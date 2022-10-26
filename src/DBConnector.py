import mysql.connector
import pandas as pd

"""
// Name        : DBConnector.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : La classe DBConnector modella la connessione al DB, istanziandola tramite costruttore e chiudendola
tramite metodo "closeConnection(). Fornisce un metodo che effettua la query sulla tabella Receipt del DB.
"""


class DBConnector:
    __mydb = mysql.connector.MySQLConnection()

    # Costruttore
    def __init__(self, host="localhost", username="root", password="", database="churn_retail_db"):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__database = database
        self.__mydb = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )

    # Metodo che chiude la connessione al DB
    def closeConnection(self):
        self.__mydb.close()

    # Metodo che effettua la query estraendo le ricevute del giorno
    def extractReceipts(self, gg):
        cursor = self.__mydb.cursor()
        cursor.execute("SELECT * FROM Receipts WHERE DATE(T_Receipt) = %s ORDER BY K_Member, T_Receipt ASC",
                       [gg.isoformat()])
        rows = cursor.fetchall()
        if len(rows) != 0:
            columns = ["K_Receipt", "K_Member", "Quantity", "Q_Amount", "T_Receipt", "Q_Discount_Amount"]
            df = pd.DataFrame(rows)
            df.columns = columns
            return df
        else:
            return None

    def extractFirstDay(self):
        cursor = self.__mydb.cursor()
        cursor.execute("SELECT DATE(T_Receipt) FROM Receipts ORDER BY T_Receipt ASC LIMIT 1")
        rows = cursor.fetchall()
        return rows[0][0]

    def extractLastDay(self):
        cursor = self.__mydb.cursor()
        cursor.execute("SELECT DATE(T_Receipt) FROM Receipts ORDER BY T_Receipt DESC LIMIT 1")
        rows = cursor.fetchall()
        return rows[0][0]
