import os

from series.series_biuld import Series


class Chuva(Series):

    type_data = 'PLUVIOMÉTRICO'

    def __init__(self, path=os.getcwd(), source=None, *args, **kwargs):
        super().__init__(path, source, type_data=self.type_data, *args, **kwargs)
