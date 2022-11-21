"""
// Name        : OfflinePerceptron.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Classe concreta Perceptron che implementa i metodi:
                    - learn_many(x: pd.DataFrame, y: pd.Series);
                    - predict_many(x: pd.DataFrame);
                 Eredita da OfflineClassifierInterface.
"""

import numpy as np

from sklearn import linear_model
from src.classification.offline.OfflineClassifierInterface import OfflineClassifierInterface


class OfflinePerceptron(OfflineClassifierInterface):
    """
        Richiama il costruttore di linear_model.Perceptron()
    """
    def __init__(self):
        self.__model = linear_model.Perceptron()

    """
        Metodo learn che prende in input:
        - x: un ndarray contenente le features;
        - y: un ndarray contenente le variabili target.0
        Richiama il fit di Perceptron
    """
    def learn(self, x: np.ndarray, y: np.ndarray):
        self.__model = self.__model.fit(x, y)
        return self

    """
        Metodo predict che prende in input:
        - x: un ndarray contenente le features.
        Restituisce un ndarray
    """
    def predict(self, x: np.ndarray) -> np.ndarray:
        # orient="records" genera una lista dove ogni elemento è una riga del DataFrame sotto forma di dizionario
        return self.__model.predict(x)
