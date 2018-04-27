import scipy.stats as stat
import pandas as pd

from abc import ABCMeta, abstractmethod


class DistributionBiuld(object):

    __metaclass__ = ABCMeta

    def __init__(self, title, forma, localizacao, escala):
        self.title = title
        self.forma = forma
        self.localizacao = localizacao
        self.escala = escala

    def plot(self, type_function):
        if type_function == 'density':
            return self.density()
        elif type_function == 'cumulative':
            return self.cumulative()

    def _data(self):
        prob = []
        for i in range(1, 1000):
            prob.append(i/1000)

        quantiles = stat.genpareto.ppf(prob, self.forma,
                                        loc=self.localizacao,
                                        scale=self.escala)

        return pd.DataFrame(quantiles, index=prob, columns=[self.title])

    @abstractmethod
    def cumulative(self):
        pass

    @abstractmethod
    def density(self):
        pass