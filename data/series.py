import os
import pandas as pd

from abc import abstractmethod, ABCMeta

from file import *


class Series(object):

    __metaclass__ = ABCMeta
    fonts = {
        "ONS": ons.Ons,
        "ANA": ana.Ana
    }

    def __init__(self, path=os.getcwd(), font=None, *args, **kwargs):
        self.path = path
        if font in self.fonts:
            self.data = self.fonts[font](self.path, *args, **kwargs).data
        else:
            raise KeyError('Font not suported!')

    @abstractmethod

    def month_start_year_hydrologic(self):
        pass

    @abstractmethod
    def date(self, date_start=None, date_end=None):
        if date_start is not None and date_end is not None:
            self.date_start = pd.to_datetime(date_start, dayfirst=True)
            self.date_end = pd.to_datetime(date_end, dayfirst=True)
            self.data = self.data.loc[self.date_start:self.date_end]
        elif date_start is not None:
            self.date_start = pd.to_datetime(date_start, dayfirst=True)
            self.data = self.data.loc[self.date_start:]
        elif date_end is not None:
            self.date_end = pd.to_datetime(date_end, dayfirst=True)
            self.data = self.data.loc[:self.date_end]
