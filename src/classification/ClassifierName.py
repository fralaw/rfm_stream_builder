from enum import Enum, unique


@unique
class ClassifierName(Enum):
    ADAP_RANDOM_FOREST = 'AdaptiveRandomForestClassifier'
    HOEFFDING_ADAPTIVE_TREE = 'HoeffdingAdaptiveTreeClassifier'
    PERCEPTRON = 'Perceptron'
    LOGISTIC_REGRESSION = 'LogisticRegression'
