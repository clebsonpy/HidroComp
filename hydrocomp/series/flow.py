import os
import calendar as cal
import pandas as pd

from hydrocomp.series.series_biuld import SeriesBuild
from hydrocomp.series.parcial import Parcial
from hydrocomp.series.maximum import Maximum
from hydrocomp.graphics.hydrogram_clean import HydrogramClean
from hydrocomp.graphics.hydrogram_by_year import HydrogramYear


class Flow(SeriesBuild):

    type_data = 'FLUVIOMÉTRICO'

    def __init__(self, data=None, path=os.getcwd(), source=None, *args, **kwargs):
        super().__init__(data, path, source, type_data=self.type_data, *args, **kwargs)
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

    def simulation_withdraw(self, criterion, rate, months=None):
        if type(months) is not list and months is not None:
            raise TypeError

        if criterion == 'q90':
            data = self.data.copy()
            data.rename(columns={self.station: "withdraw"}, inplace=True)
            withdraw = (self.quantile(percentile=0.1) * (rate / 100)).values[0]
            if months is None:
                data = data - withdraw
                data.loc[data["withdraw"] < 0, "withdraw"] = 0
                return data
            else:
                for i in self.data[self.station].index:
                    if i.month in months:
                        data.at[i, "withdraw"] = self.data[self.station][i] - withdraw
                        data.loc[data["withdraw"] < 0, "withdraw"] = 0
                return data
        else:
            return None

    def hydrogram(self, width=None, height=None, size_text=None, title=None):
        if self.station is None:
            hydrogram = HydrogramClean(self.data, width=width, height=height, size_text=size_text, title=title)
            fig, data = hydrogram.plot()
        else:
            hydrogram = HydrogramClean(self.data[self.station], width=width, height=height, size_text=size_text,
                                       title=title)
            fig, data = hydrogram.plot()
        return fig, data

    def hydrogram_year(self, width=None, height=None, size_text=None, title=None):
        self.month_start_year_hydrologic()
        idx = [i for i in self.data.index if i.month == 2 and i.day == 29]
        data = self.data.drop(index=idx)
        data = data.groupby(pd.Grouper(freq=self.month_abr))
        hydrogram = HydrogramYear(data, width=width, height=height, title=title, size_text=size_text)
        fig, data = hydrogram.plot()
        return fig, data
