import os

from hidrocomp.series.series_build import SeriesBuild
from hidrocomp.graphics.hydrogram_clean import HydrogramClean


class Rainfall(SeriesBuild):

    type_data = 'PLUVIOMÉTRICO'
    data_type = 'rainfall'

    def __init__(self, data=None, path_file=None, station=None, source=None, *args, **kwargs):
        super().__init__(data=data, path=path_file, station=station, source=source, type_data=self.type_data, *args,
                         **kwargs)

    def _month_start_year_hydrologic(self):
        pass

    # def hydrogram(self, title, threshold=None, save=False, width=None, height=None, size_text=16, color=None):
    #     if self.station is None:
    #         hydrogram = HydrogramClean(self.data, threshold=threshold, width=width, height=height, size_text=size_text,
    #                                    title=title, data_type=self.data_type)
    #         fig, data = hydrogram.plot()
    #     else:
    #         hydrogram = HydrogramClean(self.data[self.station], threshold=threshold, width=width, height=height,
    #                                    size_text=size_text, title=title, data_type=self.data_type)
    #         fig, data = hydrogram.plot()
    #     return fig, data
