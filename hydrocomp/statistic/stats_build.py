from hydrocomp import statistic as e
from abc import ABCMeta, abstractmethod

class StatsBuild(metaclass=ABCMeta):
    
    dist = None
    def __init__(self, data=None,  shape=None, loc=None, scale=None):
        if data is None:
            if shape is None or loc is None or scale is None:
                raise e.DataNotExist("Parâmetros não  informados", 12)
            else:
                self.shape = shape
                self.loc = loc
                self.scale = scale
                self.dist = self.dist(c=self.shape, loc=self.loc, scale=self.scale)
        else:
            self.data = data
            self.dist = None

    def plot_pdf(self):
        pass

    def plot_cdf(self):
        pass

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
    def mvs(self):
        pass

    @abstractmethod
    def mml(self):
        pass