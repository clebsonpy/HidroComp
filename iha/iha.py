import pandas as pd
import calendar as cal

class IHA:

    def __init__(self, data):
        self.data = data

    def rva(self):
        pass

    def mean(self):
        pass

    def std(self):
        pass

    def mean_month(self):
        years = self.data.groupby(pd.Grouper(freq='A'))
        data = pd.DataFrame()
        for year in years:
            aux = year[1].groupby(pd.Grouper(freq='M')).mean()
            df = pd.DataFrame({year[0].year: {cal.month_name[i.month]: aux.XINGO[i] for i in aux.XINGO.index}})
            data = data.combine_first(df)
        mean_months = data.T

        mean = pd.DataFrame(mean_months.mean(), columns=['Means'])
        std = pd.DataFrame(mean_months.std() / mean_months.mean(), columns=['Coeff. of Var.'])
        iha_mean_month = mean.combine_first(std)
        return iha_mean_month

    def moving_averages(self):
        aver_data = pd.DataFrame()
        for i in [1, 3, 7, 30, 90]:
            ave_max = self.data.rolling(window=i).mean().groupby(pd.Grouper(freq='A')).max()
            ave_min = self.data.rolling(window=i).mean().groupby(pd.Grouper(freq='A')).min()
            years = ave_max.index.year
            df1 = pd.DataFrame(pd.Series(data=ave_min.values, name='%s-day minimum' % i, index=years))
            df2 = pd.DataFrame(pd.Series(data=ave_max.values, name='%s-day maximum' % i, index=years))
            aver_data = aver_data.combine_first(df1)
            aver_data = aver_data.combine_first(df2)

        mean = pd.DataFrame(aver_data.mean(), columns=['Means'])
        std = pd.DataFrame(aver_data.std() / aver_data.mean(), columns=['Coeff. of Var.'])

        iha_moving_aver = mean.combine_first(std)
        return iha_moving_aver

    def daysJulian(self, type_event):

        if type_event == "flood":
            data = pd.DatetimeIndex(self.data.groupby(pd.Grouper(freq='A')).idxmax().values)
        elif type_event == "drought":
            data = pd.DatetimeIndex(self.dataFlow.groupby(pd.Grouper(
                freq='AS-%s' % self.mesInicioAnoHidrologico()[1])).idxmin()[self.nPosto].values)

        dfDayJulian = pd.DataFrame(list(map(int, data.strftime("%j"))), index=data)
        dayJulianMedia = dfDayJulian.mean()[0]
        dayJulianCv = dfDayJulian.std()[0] / dayJulianMedia
        return dfDayJulian, dayJulianMedia, dayJulianCv