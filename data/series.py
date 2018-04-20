import os

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
    def date(self, date_start, date_end):
        pass

