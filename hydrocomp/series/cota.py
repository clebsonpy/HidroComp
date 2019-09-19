import os

from hydrocomp.series.series_biuld import SeriesBuild


class Cota(SeriesBuild):

    type_data = 'COTA'

    def __init__(self, data=None, path=os.getcwd(), source=None, *args, **kwargs):
        super().__init__(data, path, source, type_data=self.type_data, *args, **kwargs)

    def month_start_year_hydrologic(self, station):
        pass

    def plot_hydrogram(self):
        pass