from abc import ABCMeta, abstractmethod

class StatsBuild():

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def prob(self, x):
        pass

    @abstractmethod
    def value(self, p):
        pass

    @abstractmethod
    def interval(self, alpha):
        pass

    @abstractmethod
    def cdf(self):
        pass

    @abstractmethod
    def pdf(self):
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def mml(self):
        pass

    @abstractmethod
    def mom(self):
        pass
