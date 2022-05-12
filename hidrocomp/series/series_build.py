import pandas as pd
import plotly.figure_factory as FF

from abc import abstractmethod, ABCMeta
from copy import copy
from hidrocomp.files import ana, ons
from hidrocomp.graphics.gantt import Gantt
from hidrocomp.graphics.hydrogram_clean import HydrogramClean


class SeriesBuild(metaclass=ABCMeta):
    sources = {
        "ONS": ons.Ons,
        "ANA": ana.Ana,
        "SAR": ana.Sar,
    }

    def __init__(self, data=None, path=None, station=None, source=None, *args, **kwargs):
        self.path = path
        if data is not None:
            if type(data) is pd.Series:
                data = pd.DataFrame(data)
            try:
                if type(station) == list():
                    self.station = None
                    self.__return_df(data)
                elif station is not None:
                    self.station = station
                    self.__return_df(data)
                    self.data = self.data.rename(columns={self.data.columns[0]: self.station}).sort_index()
                elif len(data.columns) == 1:
                    self.__return_df(data)
                    self.station = self.data.columns[0]
                else:
                    self.__return_df(data)
                    self.station = None
            except KeyError:
                self.station = None
                self.__return_df(data)
        else:
            if type(station) == list() or len(station) == 1:
                self.station = station[0]
            elif type(station) != list():
                self.station = station
            else:
                self.station = None
            if source in self.sources:
                self.source = source
                read = self.sources[self.source](path_file=self.path, station=self.station, *args, **kwargs)
                self.data = read.data.sort_index()
                self.inf_stations = read.inf_stations
            else:
                raise KeyError('Source not supported!')

        if source in ['ONS', 'ANA']:
            print(self.data)
            if self.data.size == 0:
                print('Dataframe is empty!')
                self.start_date, self.end_date = None, None
            else:
                self.start_date, self.end_date = self.__start_and_end()
                data_range = pd.date_range(start=self.start_date, end=self.end_date)
                _data = pd.DataFrame(index=data_range)
                self.data = _data.combine_first(self.data[self.start_date:self.end_date])

    def __return_df(self, data):
        if type(data) is type(pd.Series()):
            self.data = pd.DataFrame(data)
        else:
            self.data = data

    @abstractmethod
    def _month_start_year_hydrologic(self):
        pass

    @abstractmethod
    def hydrogram(self, title, save=False, width=None, height=None, size_text=None):
        pass

    def __start_and_end(self):
        try:
            boolean = self.data.dropna(axis=0, how='all')
        except AttributeError:
            boolean = self.data
        date = boolean.index
        return date[0], date[-1]

    def __str__(self):
        """
        """
        return self.data.__repr__()

    def __getitem__(self, val):
        """
        """
        return self.__class__(data=self.data[val].copy())

    @property
    def columns(self):
        return self.data.columns

    def copy(self, station=None):
        if station:
            return self[station]

        return copy(self)

    def date(self, start_date: str = None, end_date: str = None):
        """
        """
        if start_date is not None and end_date is not None:
            self.start_date = pd.to_datetime(start_date, dayfirst=True)
            self.end_date = pd.to_datetime(end_date, dayfirst=True)
            if self.start_date >= self.end_date:
                raise ValueError("Date start >= Date end")
            self.data = self.data.loc[self.start_date:self.end_date]
        elif start_date is not None:
            self.start_date = pd.to_datetime(start_date, dayfirst=True)
            if self.start_date >= self.data.iloc[-1].name:
                raise ValueError("Date start ({}) >= {}".format(self.start_date, self.data.iloc[-1].name))
            self.data = self.data.loc[self.start_date:]
        elif end_date is not None:
            self.end_date = pd.to_datetime(end_date, dayfirst=True)
            if self.end_date >= self.data.iloc[0].name:
                raise ValueError("Date end ({}) <= {}".format(self.end_date, self.data.iloc[0].name))
            self.data = self.data.loc[:self.end_date].copy()

        return self

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
        dic = {'Start': list_start, 'Finish': list_end}
        return pd.DataFrame(dic)

    @property
    def summary(self):
        """
        """
        return self.data.describe()

    def min(self):
        return self.data.min()

    def max(self):
        return self.data.max()

    def get_year(self, year):
        """
        Seleciona todos os dados referente ao ano.
        """
        return self.__getitem__(year)

    def get_month(self, month):
        """
        Selecina todos os dados referente ao mês
        """
        return self.data.groupby(lambda x: x.month).get_group(month)

    @property
    def mean(self):
        """
        """
        if len(self.columns) == 1:
            return self.data.mean().values[0]
        return self.data.mean().values

    @property
    def std(self):
        """
        """
        if len(self.columns) == 1:
            return self.data.std().values[0]
        return self.data.std()

    def percentage_failures(self):
        data_range = len(pd.date_range(start=self.start_date, end=self.end_date))
        null = data_range - self.data.count().values[0]

        if self.data.count().values[0] == 0:
            return None

        return null / self.data.count().values[0]

    def quantile(self, percentile):
        if len(self.columns) == 1:
            return self.data.quantile(percentile).values[0]
        return self.data.quantile(percentile).values

    def hydrogram(self, title, threshold=None, save=False, width=None, height=None, size_text=16, color=None,
                  showlegend: bool = False, language: str = 'pt'):
        pass

    def gantt(self, title=None, size_text=14):
        cont = 0
        df = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Description', 'IndexCol'])
        for i in self.data:
            df, cont = Gantt(self.data[i]).get_gantt(df, self.less_period(self.data[i]), cont)
        colors = ['#000000', '#778899']

        fig = FF.create_gantt(df, colors=colors, index_col='IndexCol', group_tasks=True)

        fig.layout.xaxis.title = "Data"
        fig.layout.title = dict(text=title, x=0.5, xanchor='center', y=0.9, yanchor='top',
                                font=dict(family='Courier New, monospace', color='#7f7f7f', size=size_text + 6))
        fig.layout.font = dict(family='Courier New, monospace', size=size_text, color='#7f7f7f')
        fig.layout.plot_bgcolor = 'rgba(0,0,0,0)'
        return fig, df
