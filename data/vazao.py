import os

from data.series import Series


class Vazao(Series):

    type_data = 'FLUVIOMÉTRICO'

    def __init__(self, path=os.getcwd(), font=None):
        super().__init__(path, font, type_data=self.type_data)


    def mes_inicio_ano_hidrologico(self, ):
