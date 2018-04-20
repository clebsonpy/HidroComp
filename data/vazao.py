import os
import calendar as cal

from data.series import Series


class Vazao(Series):

    type_data = 'FLUVIOMÉTRICO'

    def __init__(self, path=os.getcwd(), font=None):
        super().__init__(path, font, type_data=self.type_data)


    def month_start_year_hydrologic(self, n_posto):
        mean_month = [self.data[n_posto].loc[self.data.index.month == i].mean()
                    for i in range(1, 13)]
        self.month_start_year_hydrologic = 1 + mean_month.index(min(mean_month))
        self.month_start_year_hydrologic_abr = cal.month_abbr[
            self.month_start_year_hydrologic].upper()

        return self.month_start_year_hydrologic, \
               self.month_start_year_hydrologic_abr

