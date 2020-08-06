import pandas as pd
import plotly.figure_factory as FF

from abc import abstractmethod, ABCMeta

from hidrocomp.files import ana, ons
from hidrocomp.graphics.gantt import Gantt


class SeriesBuild(metaclass=ABCMeta):

    sources = {
        "ONS": ons.Ons,
        "ANA": ana.Ana,
        "SAR": ana.Sar,
    }

    def __init__(self, data=None, path=None, station=None, source=None, *args, **kwargs):
        self.path = path
        if data is not None:
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
            if type(station) != list():
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
        if self.data.size == 0:
            self.date_start, self.date_end = None, None
        else:
            self.date_start, self.date_end = self.__start_and_end()
            _data = pd.DataFrame(index=pd.date_range(start=self.date_start, end=self.date_end))
            self.data = _data.combine_first(self.data[self.date_start:self.date_end])

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

    def date(self, date_start=None, date_end=None):
        """
        """
        if date_start is not None and date_end is not None:
            self.date_start = pd.to_datetime(date_start, dayfirst=True)
            self.date_end = pd.to_datetime(date_end, dayfirst=True)
            self.data = self.data.loc[self.date_start:self.date_end]
        elif date_start is not None:
            self.date_start = pd.to_datetime(date_start, dayfirst=True)
            self.data = self.data.loc[self.date_start:]
        elif date_end is not None:
            self.date_end = pd.to_datetime(date_end, dayfirst=True)
            self.data = self.data.loc[:self.date_end].copy()

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

    def mean(self):
        """
        """
        return self.data.mean().values

    def std(self):
        """
        """
        return self.data.std()

    def quantile(self, percentile):
        return self.data.quantile(percentile).values

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
