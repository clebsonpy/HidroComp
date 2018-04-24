import os
import calendar as cal

import pandas as pd

from data.series import Series


class Vazao(Series):

    type_data = 'FLUVIOMÉTRICO'

    def __init__(self, data=None, path=os.getcwd(), font=None):
        super().__init__(data, path, font, type_data=self.type_data)

    def month_start_year_hydrologic(self, n_posto):
        mean_month = [self.data[n_posto].loc[self.data.index.month == i].mean()
                    for i in range(1, 13)]
        month_start_year_hydrologic = 1 + mean_month.index(min(mean_month))
        month_start_year_hydrologic_abr = cal.month_abbr[
            month_start_year_hydrologic].upper()
        month_n = month_start_year_hydrologic
        month_abr = month_start_year_hydrologic_abr

        return month_n, month_abr

    def annual_maximum(self, n_posto):
        print(self.month_start_year_hydrologic(n_posto)[1])
        data_by_year_hydrologic = self.data.groupby(pd.Grouper(
            freq='AS-%s' % self.month_start_year_hydrologic(n_posto)[1]))
        max_vazao = data_by_year_hydrologic[n_posto].max().values
        idx_vazao = data_by_year_hydrologic[n_posto].idxmax().values

        return pd.DataFrame(max_vazao, index=idx_vazao, columns=[n_posto])
