import numpy as np
import pandas as pd

from hidrocomp import statistic as e
from abc import ABCMeta, abstractmethod


class StatsBuild(metaclass=ABCMeta):

    parameter = None
    dist = None

    def __init__(self, data: pd.Series = None, *args, **kwargs):
        for i in kwargs:
            self.parameter[i] = kwargs[i]

        if data is None:
            if None in self.parameter.values():
                raise e.DataNotExist("Parâmetros não  informados", 12)
        else:
            self.data = data

    def plot_pdf(self):
        pass

    def plot_cdf(self):
        pass

    @abstractmethod
    def mvs(self):
        pass

    @abstractmethod
    def mml(self):
        pass

    def probs(self, x):
        if self.dist is None:
            raise e.DistributionNotExist('Distribuição não existe', 51)
        else:
            if type(x) is list:
                return [self.probs(i) for i in x]
            return self.dist.cdf(x)

    def values(self, p):
        if self.dist is None:
            raise e.DistributionNotExist('Distribuição não existe', 51)
        else:
            if type(p) is list or type(p) is np.ndarray:
                return [self.values(i) for i in p]
            return self.dist.ppf(p)

    def interval(self, alpha):
        if self.dist is None:
            raise e.DistributionNotExist('Distribuição não existe', 51)
        else:
            return self.dist.interval(alpha)

    def rvs(self, n):
        return self.values(np.random.random(n))
