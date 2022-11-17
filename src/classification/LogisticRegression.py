"""
// Name        : LogisticRegression.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 2.0
// Description : Classe concreta LogisticRegression che implementa i metodi:
                    - learn_many(x: pd.DataFrame, y: pd.Series);
                    - predict_many(x: pd.DataFrame);
                    - predict_one(x: pd.Series).
                 Eredita da ClassifierInterface
"""

import pandas as pd

from river import linear_model
from river import preprocessing
from ClassifierInterface import ClassifierInterface


class LogisticRegression(ClassifierInterface):
    """
        Metodo costruttore che inizializza il costruttore di uno StandardScaler
        Crea pipeline che contiene uno scaler e il modello che si vuole inizializzare.
        Richiama il costruttore di linear_model.LogisticRegression()
    """
    def __init__(self):

        self.__model = linear_model.LogisticRegression()

    """
        Metodo learn che prende in input:
        - un pandas.Dataframe;
        - una pandas.Series.
        Utilizza il meccanismo delle pipeline per aggiornare lo scaler ed effettuare il learn_many.
        Richiama il learn_many di LogisticRegression.
    """
    def learn(self, x: pd.DataFrame, y: pd.Series):
        # Aggiorna le medie dello scaler
        # self.__model.predict_many(x)
        self.__model = self.__model.learn_many(x, y)
        return self

    """
        Metodo predict_many che prende in input:
        - un Dataframe;
        Restituisce una pandas.Series.
        Richiama il predict_many di LogisticRegression.
    """
    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        # orient="records" genera una lista dove ogni elemento è una riga del DataFrame sotto forma di dizionario
        return self.__model.predict_many(x)

    """
        Metodo predict_one che prende in input:
        - una pandas.Series.
        Restituisce una valore booleano.
    """
    def predict_one(self, x: pd.Series) -> bool:
        return self.__model.predict_one(x)
