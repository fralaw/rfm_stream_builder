"""
// Name        : AdaptiveRandomForestClassifier.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 2.0
// Description : Classe concreta AdaptiveRandomForestClassifier che implementa i metodi:
                    - learn_many(x: pd.DataFrame, y: pd.Series);
                    - predict_many(x: pd.DataFrame);
                    - predict_one(x: pd.Series).
                 Eredita da ClassifierInterface.
"""

import pandas as pd

from river import ensemble, preprocessing, stream
from ClassifierInterface import ClassifierInterface


class AdaptiveRandomForestClassifier(ClassifierInterface):
    """
        Metodo costruttore che inizializza il costruttore di uno AdaptiveStandardScaler
        Crea pipeline che contiene uno scaler e il modello che si vuole inizializzare.
        Richiama il costruttore di ensemble.AdaptiveRandomForestClassifier()
    """
    def __init__(self):
        self.__model = preprocessing.MinMaxScaler() | ensemble.AdaptiveRandomForestClassifier()

    """
        Metodo learn che prende in input:
        - un pandas.Dataframe;
        - una pandas.Series.
        Utilizza il meccanismo delle pipeline per aggiornare lo scaler ed effettuare il learn_one.
        Richiama il learn_one di AdaptiveRandomForestClassifier.
    """
    def learn(self, x: pd.DataFrame, y: pd.Series):
        for xi, yi in stream.iter_pandas(x, y):
            # Aggiornare scaler
            self.__model.predict_one(xi)
            self.__model = self.__model.learn_one(xi, yi)
        return self

    """
        Metodo predict_many che prende in input:
        - un Dataframe;
        Restituisce una pandas.Series.
        Richiama il predict_one di AdaptiveRandomForestClassifier.
    """
    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        labels = []
        for xi in stream.iter_pandas(x):
            label = self.__model.predict_one(xi[0])
            labels.append(label)
        return pd.Series(labels)

    """
        Metodo predict_one che prende in input:
        - una pandas.Series.
        Restituisce una valore booleano.
    """
    def predict_one(self, x: pd.Series) -> bool:
        return self.__model.predict_one(x.to_dict())
