import os

from hydrocomp.series.series_build import SeriesBuild
from hydrocomp.graphics.hydrogram_clean import HydrogramClean


class Height(SeriesBuild):

    type_data = 'COTA'

    def __init__(self, data=None, path_file=os.getcwd(), source=None, *args, **kwargs):
        super().__init__(data, path_file, source, type_data=self.type_data, *args, **kwargs)

    def month_start_year_hydrologic(self):
        pass

    def plot_hydrogram(self, title, save=False, width=None, height=None, size_text=None):
        if self.station is None:
            hydrogram = HydrogramClean(self.data, width=width, height=height, size_text=size_text,
                                       title=title, y_title='Cota (m)', x_title='Data')
            fig, data = hydrogram.plot()
        else:
            hydrogram = HydrogramClean(self.data[self.station], width=width, height=height,
                                       size_text=size_text, title=title, y_title='Cota (m)', x_title='Data')
            fig, data = hydrogram.plot()
        return fig, data
