"""
// Name        : Main.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 2.0
// Description : Classe Main.
"""

import os
import matplotlib.pyplot as plt
import scikitplot as skplt

from sklearn.metrics import accuracy_score, classification_report
from OnlineLearner import OnlineLearner
from PickleLoader import PickleLoader
from ClassifierName import ClassifierName


class Main:
    """
        Metodo costruttore:
        Definisce la percentuale di train e test e istanzia i loader del train e test.
        Successivamente richiama il costruttore
    """
    def __init__(self, classifierName: str, folderPath: str, start: str = None, end: str = None):
        files = os.listdir(folderPath)
        train_percentage = int((len(files) * 70) / 100)

        train_loader = PickleLoader(folderPath, start=files[0], end=files[train_percentage])
        test_loader = PickleLoader(folderPath, start=files[train_percentage + 1], end=files[-1])

        model = OnlineLearner(classifierName)
        print("Inizio tra"
              "ining")
        model.train(train_loader)
        print("Inizio testing")
        tester = model.test(test_loader)
        acc = accuracy_score(tester.iloc[:, 0], tester.iloc[:, 1])
        report = classification_report(tester.iloc[:, 0], tester.iloc[:, 1])
        print(f'Accuracy: {acc}')
        print(f'Missclassification: {1 - acc}')
        print(report)
        skplt.metrics.plot_confusion_matrix(tester.iloc[:, 0], tester.iloc[:, 1])
        plt.title("ChurnDim = 115, PeriodDim = 60, Periods = 3\n"
                  "Pipeline: StandardScaler -> AdaptiveRandomForestClassifier")
        plt.show()
        model.toPickle("./../../serialized_models")


print("Classificatori disponibili: \n")
print(ClassifierName.ADAP_RANDOM_FOREST.value)
print(ClassifierName.HOEFFDING_ADAPTIVE_TREE.value)
print(ClassifierName.PERCEPTRON.value)
print(ClassifierName.LOGISTIC_REGRESSION.value)

val = input("Inserire scelta: ")

Main(val, './../../output')
