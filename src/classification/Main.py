import os

from OnlineLearner import OnlineLearner
from PickleLoader import PickleLoader


class Main:
    def __init__(self, classifierName: str, folderPath: str, start: str = None, end: str = None):
        files = os.listdir(folderPath)
        a = int((len(files) * 70) / 100)
        train_loader = PickleLoader(folderPath, start=files[0], end=files[a])
        test_loader = PickleLoader(folderPath, start=files[a + 1], end=files[-1])
        learner = OnlineLearner(classifierName)
        learner.train(train_loader)
        out = learner.test(test_loader)
        print(out)


Main('AdaptiveRandomForestClassifier', './../../output')
