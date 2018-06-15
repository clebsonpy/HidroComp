import os

from series.series_biuld import SeriesBiuld


class Chuva(SeriesBiuld):

    type_data = 'PLUVIOMÉTRICO'

    def __init__(self, path=os.getcwd(), source=None, *args, **kwargs):
        super().__init__(path, source, type_data=self.type_data, *args, **kwargs)
