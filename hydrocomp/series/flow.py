import os
import calendar as cal
import pandas as pd
from hydrocomp.series.exceptions import StationError

from hydrocomp.statistic.pearson3 import Pearson3
from hydrocomp.series.series_build import SeriesBuild
from hydrocomp.series.parcial import Parcial
from hydrocomp.series.maximum import Maximum
from hydrocomp.graphics.hydrogram_clean import HydrogramClean
from hydrocomp.graphics.hydrogram_by_year import HydrogramYear
from hydrocomp.graphics.permanence_curve import PermanenceCurve


class Flow(SeriesBuild):
    type_data = 'FLUVIOMÉTRICO'

    def __init__(self, data=None, path_file=os.getcwd(), source=None, *args, **kwargs):
        super().__init__(data, path_file, source, type_data=self.type_data, *args, **kwargs)
        self.month_num = 1
        self.month_abr = 'AS-JAN'

    def month_start_year_hydrologic(self):
        if self.station is None:
            mean_month = [self.data.loc[self.data.index.month == i].mean() for i in range(1, 13)]
            month_start_year_hydrologic = 1 + mean_month.index(min(mean_month))
            month_start_year_hydrologic_abr = cal.month_abbr[month_start_year_hydrologic].upper()
            self.month_num = month_start_year_hydrologic
            self.month_abr = month_start_year_hydrologic_abr
        else:
            mean_month = [self.data[self.station].loc[self.data.index.month == i].mean() for i in range(1, 13)]
            month_start_year_hydrologic = 1 + mean_month.index(min(mean_month))
            month_start_year_hydrologic_abr = cal.month_abbr[month_start_year_hydrologic].upper()
            self.month_num = month_start_year_hydrologic
            self.month_abr = 'AS-%s' % month_start_year_hydrologic_abr

        return self.month_num, self.month_abr

    def maximum(self):
        maximum = Maximum(obj=self, station=self.station)

        return maximum

    def parcial(self, type_threshold, type_event, type_criterion, value_threshold, **kwargs):
        parcial = Parcial(obj=self, type_threshold=type_threshold, type_event=type_event, type_criterion=type_criterion,
                          value_threshold=value_threshold, **kwargs)

        return parcial

    def simulation_withdraw(self, criterion, rate, months=None, value=None):
        if type(months) is not list and months is not None:
            raise TypeError

        if criterion == 'q90':
            data = self.data.copy()
            if value is None:
                withdraw = (self.quantile(percentile=0.1) * (rate / 100)).values[0]
            else:
                withdraw = (value * (rate / 100)).values[0]

            if months is None:
                name = "withdraw_{}_{}_{}".format(rate, criterion, 'all')
                data.rename(columns={self.station: name}, inplace=True)
                data = data - withdraw
                data.loc[data[name] < 0, name] = 0
                return data
            else:
                name = "withdraw_{}_{}_{}".format(rate, criterion, 'months')
                data.rename(columns={self.station: name}, inplace=True)
                for i in self.data[self.station].index:
                    if i.month in months:
                        data.at[i, name] = self.data[self.station][i] - withdraw
                        data.loc[data[name] < 0, name] = 0
                return data
        else:
            return None

    def plot_hydrogram(self, title, save=False, width=None, height=None, size_text=None):
        if self.station is None:
            hydrogram = HydrogramClean(self.data, width=width, height=height, size_text=size_text,
                                       title=title, y_title='Vazão (m³/s)', x_title='Data')
            fig, data = hydrogram.plot()
        else:
            hydrogram = HydrogramClean(self.data[self.station], width=width, height=height,
                                       size_text=size_text, title=title, y_title='Vazão (m³/s)', x_title='Data')
            fig, data = hydrogram.plot()
        return fig, data

    def hydrogram_year(self, title, width=None, height=None, size_text=None):
        self.month_start_year_hydrologic()
        idx = [i for i in self.data.index if i.month == 2 and i.day == 29]
        data = self.data.drop(index=idx)
        data = data.groupby(pd.Grouper(freq=self.month_abr))
        hydrogram = HydrogramYear(data, width=width, height=height, title=title, size_text=size_text)
        fig = hydrogram.plot()
        return fig

    def permanence_curve(self, width=None, height=None, size_text=None, title=None):
        if self.station is None:
            raise StationError
        permanence = PermanenceCurve(self.data[self.station], width=width, height=height, size_text=size_text,
                                     title=title)
        fig, data = permanence.plot()
        return fig, data

    def get_month_name(self):
        months = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                  9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        return months[self.month_num]

    def flow_min(self, method):
        if method == 'q90':
            return self.quantile(0.1)
        elif method == 'q95':
            return self.quantile(0.05)
        elif method == 'q710':
            qmin = self.data.rolling(7).mean().groupby(pd.Grouper(freq='AS-JAN')).min()
            prop = 1 / 10
            dist = Pearson3(qmin[self.station].values)
            dist.mml()
            return dist.values(prop)
