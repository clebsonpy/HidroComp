import os
import pandas as pd
import plotly.figure_factory as FF

from abc import abstractmethod, ABCMeta

from files import *
from graphics.gantt import Gantt


class SeriesBiuld(object, metaclass=ABCMeta):

    sources = {
        "ONS": ons.Ons,
        "ANA": ana.Ana
    }

    def __init__(self, data=None, path=os.getcwd(), source=None, delete_null=False, *args, **kwargs):
        self.path = path
        if data is not None:
            if delete_null is True:
                self.data = data.dropna(axis=0, how='all')
            else:
                self.data = data
        else:
            if source in self.sources:
                self.source = source
                if delete_null is True:
                    self.data = self.sources[self.source](self.path, *args, **kwargs).data.dropna(axis=0, how='all')
                else:
                    self.data = self.sources[self.source](self.path, *args, **kwargs).data
            else:
                raise KeyError('Source not supported!')
        print(self.data)
        self.date_start = self.data.index[0]
        self.date_end = self.data.index[-1]
        _data = pd.DataFrame(index=pd.date_range(start=self.date_start, end=self.date_end))
        self.data = _data.combine_first(self.data)

    @abstractmethod
    def month_start_year_hydrologic(self, station):
        pass

    @abstractmethod
    def plot_hydrogram(self):
        pass

    def __str__(self):
        """
        """
        return self.data.__repr__()

    def __getitem__(self, val):
        """
        """
        return self.__class__(data = self.data[val].copy())

    def date(self, date_start=None, date_end=None):
        """
        """
        if date_start is not None and date_end is not None:
            date_start = pd.to_datetime(date_start, dayfirst=True)
            date_end = pd.to_datetime(date_end, dayfirst=True)
            return self.__class__(data = self.data.loc[date_start:date_end].copy())
        elif date_start is not None:
            date_start = pd.to_datetime(date_start, dayfirst=True)
            return self.__class__(data = self.data.loc[date_start:].copy())
        elif date_end is not None:
            date_end = pd.to_datetime(date_end, dayfirst=True)
            return self.__class__(data = self.data.loc[:date_end].copy())

    def less_period(self, data):
        """
        """
        aux = list()
        list_start = list()
        list_end = list()
        gantt_bool = data.isnull()
        for i in gantt_bool.index:
            if ~gantt_bool.loc[i]:
                aux.append(i)
            elif len(aux) > 2 and gantt_bool.loc[i]:
                list_start.append(aux[0])
                list_end.append(aux[-1])
                aux = []
        if len(aux) > 0:
            list_start.append(aux[0])
            list_end.append(aux[-1])
        dic = {'Inicio': list_start, 'Fim': list_end}
        return pd.DataFrame(dic)

    def summary(self):
        """
        """
        return self.data.describe()

    def get_year(self, year):
        """
        Seleciona todos os dados referente ao ano.
        """
        return self.__getitem__(year)

    def get_month(self, month):
        """
        Selecina todos os dados referente ao mês
        """
        return self.__class__(data=self.data.groupby(lambda x: x.month).get_group(month))

    def mean(self):
        """
        """
        return self.data.mean()

    def std(self):
        """
        """
        return self.data.std()

    def gantt(self, name):
        cont = 0
        df = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Description', 'IndexCol'])
        for i in self.data:
            df, cont = Gantt(self.data[i]).get_gantt(df, self.less_period(self.data[i]), cont)
        fig = FF.create_gantt(df, colors = '#000000', group_tasks=True, title=name)
        return fig
