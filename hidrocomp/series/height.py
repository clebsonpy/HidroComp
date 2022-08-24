import os
import calendar as cal
import pandas as pd

from hidrocomp.series.maximum import MaximumHeight
from hidrocomp.series.minimum import MinimumHeight
from hidrocomp.series.series_build import SeriesBuild
from hidrocomp.graphics.hydrogram_clean import HydrogramClean


class Height(SeriesBuild):

    type_data = 'COTA'
    data_type = 'height'

    def __init__(self, data=None, path_file=None, station=None, source=None, *args, **kwargs):
        super().__init__(data=data, path=path_file, station=station, source=source, type_data=self.type_data, *args,
                         **kwargs)
        self.__month_num_flood = None
        self.__month_abr_flood = None
        self.__month_num_drought = None
        self.__month_abr_drought = None

    def _month_start_year_hydrologic(self):
        if self.__month_num_flood is None:
            if self.station is None:
                raise TypeError("Define a station!")
            else:
                data = pd.DataFrame(self.data[self.station])
                mean_month = pd.DataFrame([data.loc[data.index.month == i].mean() for i in range(1, 13)])
                month_start_year_hydrologic = 1 + mean_month.idxmin().values[0]
                month_start_year_hydrologic_abr_flood = cal.month_abbr[month_start_year_hydrologic].upper()

                self.__month_num_flood = month_start_year_hydrologic
                self.__month_abr_flood = 'AS-%s' % month_start_year_hydrologic_abr_flood

                self.__month_num_drought = month_start_year_hydrologic - 6
                self.__month_abr_drought = 'AS-%s' % cal.month_abbr[self.__month_num_drought].upper()
        else:
            if self.__month_num_flood > 6:
                self.__month_num_drought = self.__month_num_flood - 6
            else:
                self.__month_num_drought = self.__month_num_flood + 6

            self.__month_abr_flood = 'AS-%s' % cal.month_abbr[self.__month_num_flood].upper()
            self.__month_abr_drought = 'AS-%s' % cal.month_abbr[self.__month_num_drought].upper()

        return self.__month_num_flood, self.__month_abr_flood, self.__month_num_drought, self.__month_abr_drought

    @property
    def month_num_flood(self) -> int:
        return self._month_start_year_hydrologic()[0]

    @month_num_flood.setter
    def month_num_flood(self, month: int):
        self.__month_num_flood = month

    @property
    def month_abr_flood(self) -> str:
        return self._month_start_year_hydrologic()[1]

    @property
    def month_num_drought(self) -> int:
        return self._month_start_year_hydrologic()[2]

    @property
    def month_abr_drought(self) -> str:
        return self._month_start_year_hydrologic()[3]

    def minimum(self) -> MinimumHeight:
        minimum = MinimumHeight(height=self, station=self.station)

        return minimum

    def maximum(self) -> MaximumHeight:
        maximum = MaximumHeight(height=self, station=self.station)

        return maximum

    def cotagram(self, title, threshold=None, width=None, height=None, size_text=16, color=None, **kwargs):
        if self.station is None:
            cotagram = HydrogramClean(data=self.data, threshold=threshold, width=width, height=height,
                                      size_text=size_text, title=title, color=color, data_type=self.data_type, **kwargs)
            fig, data = cotagram.plot()
        else:
            cotagram = HydrogramClean(data=self.data[self.station], threshold=threshold, width=width, height=height,
                                      size_text=size_text, title=title, color=color, data_type=self.data_type, **kwargs)
            fig, data = cotagram.plot()

        return fig, data
