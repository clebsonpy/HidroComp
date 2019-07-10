from abc import ABCMeta, abstractmethod

class StatsBuild():

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
    def fit(self, estimador):
        pass

    @abstractmethod
    def mml(self):
        pass

    @abstractmethod
    def mom(self):
        pass
