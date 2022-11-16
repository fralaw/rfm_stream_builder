"""
// Name        : ClassifierInterface.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 2.0
// Description : Interfaccia ClassifierInterface per permettere alle classi Perceptron, LogisticRegression,
                 AdaptiveRandomForestClassifier e HoeffdingAdaptiveTreeClassifier di implementare i metodi sottostanti.
"""

import pandas as pd


class ClassifierInterface:
    """
        Metodo learn che prende in input:
        - un pandas.Dataframe;
        - una pandas.Series.
    """
    def learn(self, x: pd.DataFrame, y: pd.Series):
        pass

    """
        Metodo predict_many che prende in input:
        - un Dataframe;
        Restituisce una pandas.Series.
    """
    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        pass

    """
        Metodo predict_one che prende in input:
        - una pandas.Series.
        Restituisce una valore booleano.
    """
    def predict_one(self, x: pd.Series) -> bool:
        pass
