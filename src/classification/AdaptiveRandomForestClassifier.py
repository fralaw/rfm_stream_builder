"""
// Name        : AdaptiveRandomForestClassifier.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 3.0
// Description : Classe concreta AdaptiveRandomForestClassifier che eredita da StreamClassifier.
"""
from river import ensemble
from StreamClassifier import StreamClassifier
import pandas as pd


class AdaptiveRandomForestClassifier(StreamClassifier):
    def __init__(self):
        self.__model = ensemble.AdaptiveRandomForestClassifier()

    def learn(self, x: pd.DataFrame, y: pd.Series):
        for index, row in x.iterrows():
            x_row = row.apply(pd.to_numeric, downcast='float').to_dict()
            print(x_row)
            y_row = y[index]
            print(y_row)
            self.__model.learn_one(x_row, y_row)

    def predict_many(self, x: pd.DataFrame) -> pd.Series:
        labels = []
        for index, row in x.iterrows():
            x_row = row.apply(pd.to_numeric, downcast='float').to_dict()
            label = self.__model.predict_one(x_row)
            labels.append(label)
        return pd.Series(labels)

    def predict_one(self, x: pd.Series) -> bool:
        return self.__model.predict_one(x.to_dict())
