import os

from data.series import Series


class Vazao(Series):

    type_data = 'FLUVIOMÉTRICO'

    def __init__(self, path=os.getcwd(), font=None):
        super().__init__(path, font, type_data=self.type_data)


    def month_start_year_hydrologic(self):
        pass
