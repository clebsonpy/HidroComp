import pandas as pd

from abc import ABCMeta, abstractmethod


class HydrogramBiuld(object, metaclass=ABCMeta):

    @abstractmethod
    def plot(self):
        pass
