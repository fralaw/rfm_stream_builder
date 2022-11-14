"""
// Name        : ClassifierInterface.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Interfaccia ClassifierInterface per permettere alle classi astratte StreamClassifier e
                 IncrementalClassifier di implementare i metodi sottostanti.
"""

import pandas as pd


class ClassifierInterface:
    def learn(self, x: pd.DataFrame, y: pd.Series):
        pass

    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        pass

    def predict_one(self, x: pd.Series) -> bool:
        pass
