import os
import calendar as cal

from series.series_biuld import SeriesBuild
from series.parcial import Parcial
from series.maximum import Maximum
from graphics.hydrogram_clean import HydrogramClean
from graphics.gantt import Gantt


class Flow(SeriesBuild):

    type_data = 'FLUVIOMÉTRICO'

    def __init__(self, data=None, path=os.getcwd(), source=None, *args, **kwargs):
        self.month_num = 1
        self.month_abr = 'jan'
        super().__init__(data, path, source, type_data=self.type_data, *args, **kwargs)

    def month_start_year_hydrologic(self):
        mean_month = [self.data[self.station].loc[self.data.index.month == i].mean() for i in range(1, 13)]
        month_start_year_hydrologic = 1 + mean_month.index(min(mean_month))
        month_start_year_hydrologic_abr = cal.month_abbr[month_start_year_hydrologic].upper()
        self.month_num = month_start_year_hydrologic
        self.month_abr = month_start_year_hydrologic_abr

        return self.month_num, 'AS-%s' % self.month_abr

    def maximum(self):
        maximum = Maximum(obj=self, station=self.station)

        return maximum

    def parcial(self, type_threshold, type_event, type_criterion, value_threshold, **kwargs):
        parcial = Parcial(obj=self, type_threshold=type_threshold, type_event=type_event, type_criterion=type_criterion,
                          value_threshold=value_threshold, **kwargs)

        return parcial

    def plot_hydrogram(self):
        if self.station is None:
            hydrogram = HydrogramClean(self.data)
            fig, data = hydrogram.plot()
        else:
            hydrogram = HydrogramClean(self.data[self.station])
            fig, data = hydrogram.plot()
        return fig, data
