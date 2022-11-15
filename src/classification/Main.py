"""
// Name        : Main.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 1.0
// Description : Classe Main.
"""
import enum
import os
import matplotlib.pyplot as plt
import scikitplot as skplt

from OnlineLearner import OnlineLearner
from PickleLoader import PickleLoader
from ClassifierName import ClassifierName


class Main:
    def __init__(self, classifierName: str, folderPath: str, start: str = None, end: str = None):
        files = os.listdir(folderPath)
        train_percentage = int((len(files) * 70) / 100)

        train_loader = PickleLoader(folderPath, start=files[0], end=files[train_percentage])
        test_loader = PickleLoader(folderPath, start=files[train_percentage + 1], end=files[-1])

        model = OnlineLearner(classifierName)
        model.train(train_loader)
        tester = model.test(test_loader)
        skplt.metrics.plot_confusion_matrix(tester.iloc[:, 0], tester.iloc[:, 1])
        plt.show()


# cProfile.run("Main('AdaptiveRandomForestClassifier', './../../output')")
print(ClassifierName.ADAP_RANDOM_FOREST.value)
print(ClassifierName.HOEFFDING_ADAPTIVE_TREE.value)
print(ClassifierName.PERCEPTRON.value)
print(ClassifierName.LOGISTIC_REGRESSION.value)

val = input("Inserire scelta: ")

Main(val, './../../output')
