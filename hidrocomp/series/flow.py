import calendar as cal
import pandas as pd

from hidrocomp.series.exceptions import StationError
from hidrocomp.statistic.pearson3 import Pearson3
from hidrocomp.series.series_build import SeriesBuild
from hidrocomp.series.parcial import Parcial
from hidrocomp.series.maximum import Maximum
from hidrocomp.series.minimum import Minimum
from hidrocomp.eflow import IHA
from hidrocomp.graphics import RatingCurve, HydrogramYear, HydrogramClean


class Flow(SeriesBuild):
    type_data = 'FLUVIOMÉTRICO'

    def __init__(self, data=None, path_file=None, station=None, source=None, *args, **kwargs):
        super().__init__(data=data, path=path_file, station=station, source=source,
                         type_data=self.type_data, *args, **kwargs)
        self.month_num_flood = 1
        self.month_abr_flood = 'AS-JAN'
        self.month_num_drought = 12
        self.month_abr_drought = 'AS-DEC'

    def month_start_year_hydrologic(self):
        if self.station is None:
            mean_month = pd.DataFrame([self.data.loc[self.data.index.month == i].mean() for i in range(1, 13)])
            month_start_year_hydrologic = 1 + mean_month.idxmin().values[0]
            month_start_year_hydrologic_abr_flood = cal.month_abbr[month_start_year_hydrologic].upper()
        else:
            data = pd.DataFrame(self.data[self.station])
            mean_month = pd.DataFrame([data.loc[data.index.month == i].mean() for i in range(1, 13)])
            month_start_year_hydrologic = 1 + mean_month.idxmin().values[0]
            month_start_year_hydrologic_abr_flood = cal.month_abbr[month_start_year_hydrologic].upper()

        self.month_num_flood = month_start_year_hydrologic
        self.month_abr_flood = 'AS-%s' % month_start_year_hydrologic_abr_flood

        self.month_num_drought = month_start_year_hydrologic - 6
        month_start_year_hydrologic_abr_drought = cal.month_abbr[self.month_num_drought].upper()
        self.month_abr_drought = 'AS-%s' % month_start_year_hydrologic_abr_drought
        return self.month_num_flood, self.month_abr_flood, self.month_num_drought, self.month_abr_drought

    def minimum(self):
        minimum = Minimum(obj=self, station=self.station)

        return minimum

    def maximum(self):
        maximum = Maximum(obj=self, station=self.station)

        return maximum

    def parcial(self, type_threshold, type_event, type_criterion, value_threshold, **kwargs):
        parcial = Parcial(station=self.station, obj=self, type_threshold=type_threshold, type_event=type_event,
                          type_criterion=type_criterion, value_threshold=value_threshold, **kwargs)

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

    def hydrogram(self, title, threshold=None, save=False, width=None, height=None, y_title='Vazão (m³/s)',
                  x_title='Data', size_text=16, color=None):
        if self.station is None:
            hydrogram = HydrogramClean(self.data, threshold=threshold, width=width, height=height, size_text=size_text,
                                       title=title, y_title=y_title, x_title=x_title, color=color)
            fig, data = hydrogram.plot()
        else:
            hydrogram = HydrogramClean(self.data[self.station], threshold=threshold, width=width, height=height,
                                       size_text=size_text, title=title, y_title=y_title, x_title=x_title, color=color)
            fig, data = hydrogram.plot()
        return fig, data

    def iha(self, status=None, date_start: str = None, date_end: str = None, statistic="no-parametric",
            central_metric="mean", month_water: int = None, variation_metric: str = "std", type_threshold="stationary",
            type_criterion: str = None, threshold_high: float = None, threshold_low: float = None, **kwargs) -> IHA:
        """
        @param status:
        @param date_start:
        @param date_end:
        @param statistic:
        @param central_metric:
        @param month_water:
        @param variation_metric:
        @param type_threshold:
        @param type_criterion:
        @param threshold_high:
        @param threshold_low:
        @return:
        """
        iha = IHA(flow=self, month_water=month_water, status=status, date_start=date_start, date_end=date_end,
                  statistic=statistic, central_metric=central_metric, variation_metric=variation_metric,
                  type_threshold=type_threshold, type_criterion=type_criterion, threshold_high=threshold_high,
                  threshold_low=threshold_low, **kwargs)
        return iha

    def power_energy(self, efficiency: int, gravity: float, hydraulic_head: float, station: str = None) -> pd.Series:
        if len(self.columns) > 1:
            if station is None:
                raise AttributeError("Station is None")
            else:
                data = self.data[station]
        else:
            data = self.data
        const = efficiency * gravity * hydraulic_head
        pot = data.multiply(const)
        return pot

    def hydrogram_year(self, title="", threshold=None, width=None, height=None, size_text=16):
        self.month_start_year_hydrologic()
        idx = [i for i in self.data.index if i.month == 2 and i.day == 29]
        data = self.data.drop(index=idx)
        data = data.groupby(pd.Grouper(freq=self.month_abr_flood))
        hydrogram = HydrogramYear(data=data, threshold=threshold, width=width, height=height, title=title,
                                  size_text=size_text)
        fig, data = hydrogram.plot()
        return fig, data

    def rating_curve(self, width=None, height=None, size_text=None, title=None):
        if self.station is None:
            raise StationError
        permanence = RatingCurve(self.data[self.station], width=width, height=height, size_text=size_text,
                                 title=title)
        fig, data = permanence.plot()
        return fig, data

    def get_month_name(self):
        months = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                  9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        return months[self.month_num_flood]

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
