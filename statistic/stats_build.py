from abc import ABCMeta, abstractmethod

class StatsBuild():

    @abstractmethod
    def probs(self, x):
        pass

    @abstractmethod
    def values(self, p):
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
    def mvs(self):
        pass

    @abstractmethod
    def mml(self):
        pass
