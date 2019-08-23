from iha.exceptions import NotStation, NotStatistic, NotRva, NotTypePandas
import pandas as pd
import calendar as cal
import numpy as np
from series.flow import Flow


class IHA:

    def __init__(self, data, month_water=None, station=None, status=None, date_start=None, date_end=None,
                 statistic=None, central_metric=None, variation_metric=None):
        """
        :param data: pandas Series
        :param month_water: initial month water (int: referent the month, ex.: 1 for Jan, 2 for Fev)
        :param station: station of data
        :param status: 'pre' or 'pos'
        :param date_start: Date of start application ('dd/mm/aaaa')
        :param date_end: Date of end application ('dd/mm/aaaa')
        :param statistic: 'non-parametric or parametric'
        :param central_metric: 'mean or median'
        :param variation_metric: 'str' or 'cv'
        """
        self.flow = Flow(data)
        self.status = status
        self.station = self.get_station(station)
        self.month_start = self.get_month_start(month_water)
        self.date_start = pd.to_datetime(date_start, dayfirst=True)
        self.date_end = pd.to_datetime(date_end, dayfirst=True)
        self.statistic = statistic
        self.central_metric = central_metric
        self.variation_metric = variation_metric

    # <editor-fold desc="Calculation of statistical metrics">
    @staticmethod
    def metric_stats(group, central_metric, variation_metric):
        if central_metric == 'mean':
            mean = pd.DataFrame(group.mean(), columns=['Means'])
        elif central_metric == 'median':
            mean = pd.DataFrame(group.median(), columns=['Means'])
        else:
            raise NotStatistic('Not exist statistic {}: use {} or {}'.format(central_metric, 'mean', 'median'), line=40)
        if variation_metric == 'cv':
            cv = pd.DataFrame(group.std() / group.mean(), columns=['Coeff. of Var.'])
        elif variation_metric == 'std':
            cv = pd.DataFrame(group.std(), columns=['Coeff. of Var.'])
        else:
            raise NotStatistic('Not exist statistic {}: use {} or {}'.format(variation_metric, 'cv', 'std'), line=46)

        stats = mean.combine_first(cv)
        return stats
    # </editor-fold>

    # <editor-fold desc="Check type rate"
    @staticmethod
    def check_rate(value1, value2, type_rate):
        if type_rate == 'Rise rate':
            return value1 < value2
        elif type_rate == 'Fall rate':
            return value1 > value2
    # </editor-fold>

    # <editor-fold desc="Range of Variability Approach Frequency">
    @staticmethod
    def rva_frequency(data_group, lower_line, upper_line):
        count = pd.DataFrame(columns=['Lower', 'Median', 'Upper'])
        full = pd.DataFrame(columns=['Sum'])
        for i in data_group:
            if upper_line[i] == 0 or lower_line[i] == 0:
                count.at[i, 'Lower'] = 0
                count.at[i, 'Upper'] = 0
                count.at[i, 'Median'] = 0
            else:
                boolean_lower = pd.DataFrame(data_group[i].isin(data_group.loc[data_group[i] < lower_line[i], i]))
                boolean_upper = pd.DataFrame(data_group[i].isin(data_group.loc[data_group[i] > upper_line[i], i]))
                boolean_median = pd.DataFrame(data_group[i].isin(data_group.loc[
                                                                     boolean_lower[i] == boolean_upper[i], i]))
                full.at[i, 'Sum'] = data_group[i].count()
                count.at[i, 'Lower'] = boolean_lower[i].loc[boolean_lower[i] == True].count()/full['Sum'][i]
                count.at[i, 'Upper'] = boolean_upper[i].loc[boolean_upper[i] == True].count()/full['Sum'][i]
                count.at[i, 'Median'] = boolean_median[i].loc[boolean_median[i] == True].count()/full['Sum'][i]
        return count
    # </editor-fold>

    # <editor-fold desc="Range of Variability Approach Line">
    def rva_line(self, data_group, boundaries):
        if (type(data_group) == type(pd.DataFrame())) or (type(data_group) == type(pd.Series())):
            if self.status == 'pre':
                lower_line = pd.Series(name='lower_line')
                upper_line = pd.Series(name='upper_line')
                if self.statistic == 'non-parametric':
                    for i in data_group:
                        lower_line.at[i] = data_group[i].quantile((50 - boundaries) / 100)
                        upper_line.at[i] = data_group[i].quantile((50 + boundaries) / 100)
                    return lower_line, upper_line
                elif self.statistic == 'parametric':
                    for i in data_group:
                        lower_line.at[i] = data_group[i].mean() - data_group[i].std()
                        upper_line.at[i] = data_group[i].mean() + data_group[i].std()
                    return lower_line, upper_line
                else:
                    raise NotStatistic('Not exist statistic {}: use {} or {}'.format(
                        self.statistic, 'non-parametric', 'parametric'), line=91)
            else:
                raise NotRva('Use RVA in data pre-impact', line=93)
        else:
            raise NotTypePandas('Not use type data {}: Use {} or {}'.format(type(data_group), type(pd.DataFrame()),
                                                                            type(pd.Series())), line=96)

    # </editor-fold>

    # <editor-fold desc="Return Station">
    def get_station(self, station):
        if len(self.flow.data.columns.values) != 1:
            if station is None:
                raise NotStation("Station requirement")
            else:
                if station in self.flow.data.columns.values:
                    return station
                else:
                    raise NotStation("Not station")
        else:
            get_station = self.flow.data.columns.values[0]
            self.flow.data = pd.DataFrame(self.flow.data[get_station])

            return get_station

    # </editor-fold>

    # <editor-fold desc= "Return Month Water">
    def get_month_start(self, month_water=None):
        """
        :param month_water:
        :return self.month_water:
        """
        if month_water is None:
            return self.flow.month_start_year_hydrologic(station=self.station)
        else:
            return month_water, 'AS-%s' % cal.month_abbr[month_water].upper()

    # </editor-fold>

    # <editor-fold desc="Group 1: Magnitude of monthly water conditions">
    def magnitude(self):
        years = self.flow.data.groupby(pd.Grouper(freq=self.month_start[1]))
        data = pd.DataFrame()
        for year in years:
            aux = year[1].groupby(pd.Grouper(freq='M')).mean()
            df = pd.DataFrame({year[0].year: {
                cal.month_name[i.month]: aux[self.station][i] for i in aux[self.station].index}})
            data = data.combine_first(df)
        mean_months = data.T

        return mean_months, self.metric_stats(mean_months, central_metric=self.central_metric,
                                              variation_metric=self.variation_metric)

    # </editor-fold>

    # <editor-fold desc="Group 2: Magnitude and Duration of annual extreme water conditions">
    def magnitude_and_duration(self):
        aver_data = pd.DataFrame()
        for i in [1, 3, 7, 30, 90]:
            ave_max = self.flow.data.rolling(window=i).mean().groupby(pd.Grouper(freq=self.month_start[1])).max()
            ave_min = self.flow.data.rolling(window=i).mean().groupby(pd.Grouper(freq=self.month_start[1])).min()
            years = ave_max.index.year
            df1 = pd.DataFrame(pd.Series(data=ave_min[self.station].values, name='%s-day minimum' % i, index=years))
            df2 = pd.DataFrame(pd.Series(data=ave_max[self.station].values, name='%s-day maximum' % i, index=years))
            aver_data = aver_data.combine_first(df1)
            aver_data = aver_data.combine_first(df2)
            if i == 7:
                mean_year = self.flow.data[self.station].groupby(pd.Grouper(freq=self.month_start[1])).mean().values
                base_flow = pd.DataFrame(pd.Series(data=ave_min[self.station].values / mean_year,
                                                   name='Base flow index', index=years))
                aver_data = aver_data.combine_first(base_flow)

        dic_zero = {i[0].year: i[1].loc[i[1][self.station].values == 0].sum()
                    for i in self.flow.data.groupby(pd.Grouper(freq=self.month_start[1]))}

        magn_and_duration = aver_data.combine_first(pd.DataFrame(pd.Series(data=dic_zero, name='Number of zero days')))

        return magn_and_duration, self.metric_stats(magn_and_duration, central_metric=self.central_metric,
                                                    variation_metric=self.variation_metric)

    # </editor-fold>

    # <editor-fold desc="Group 3: Timing of annual extreme water conditions">

    def timing_extreme(self):

        day_julian_max = pd.DatetimeIndex(self.flow.data[self.station].groupby(
            pd.Grouper(freq=self.month_start[1])).idxmax().values)
        day_julian_min = pd.DatetimeIndex(self.flow.data[self.station].groupby(
            pd.Grouper(freq=self.month_start[1])).idxmin().values)

        df_day_julian_max = pd.DataFrame(list(map(int, day_julian_max.strftime("%j"))), index=day_julian_max.year,
                                         columns=["Date of maximum"])
        df_day_julian_min = pd.DataFrame(list(map(int, day_julian_min.strftime("%j"))), index=day_julian_min.year,
                                         columns=["Date of minimum"])

        # combine the dfs of days julian
        timing_extreme = df_day_julian_max.combine_first(df_day_julian_min)
        return timing_extreme, self.metric_stats(timing_extreme, central_metric=self.central_metric,
                                                 variation_metric=self.variation_metric)

    # </editor-fold>

    # <editor-fold desc="Group 4: Frequency and duration of high and low pulses">
    def frequency_and_duration(self, type_threshold, type_criterion, threshold_high, threshold_low, **kwargs):

        def aux_frequency_and_duration(events):
            name = {'flood': 'High', 'drought': 'Low'}
            type_event = events.type_event
            duration_pulse = pd.DataFrame(events.peaks.groupby(
                pd.Grouper(freq=self.month_start[1])).Duration.mean()).rename(
                columns={"Duration": '{} pulse duration'.format(name[type_event])})

            pulse = pd.DataFrame(events.peaks.groupby(pd.Grouper(freq=self.month_start[1])).Duration.count()).rename(
                columns={"Duration": '{} pulse count'.format(name[type_event])})

            pulse = pulse.fillna(0)

            group = duration_pulse.combine_first(pulse)

            threshold = pd.DataFrame(pd.Series(events.threshold, name="{} Pulse Threshold".format(name[type_event])))
            return group, threshold

        events_high = self.flow.parcial(station=self.station, type_threshold=type_threshold, type_event="flood",
                                        type_criterion=type_criterion, value_threshold=threshold_high, **kwargs)

        frequency_and_duration_high, threshold_high_mag = aux_frequency_and_duration(events_high)

        events_low = self.flow.parcial(station=self.station, type_event='drought', type_threshold=type_threshold,
                                       type_criterion=type_criterion, value_threshold=threshold_low, **kwargs)
        frequency_and_duration_low, threshold_low_mag = aux_frequency_and_duration(events_low)

        frequency_and_duration = frequency_and_duration_high.combine_first(frequency_and_duration_low)
        metric_stats = self.metric_stats(frequency_and_duration, central_metric=self.central_metric,
                                         variation_metric=self.variation_metric)
        return frequency_and_duration, metric_stats, threshold_low_mag, threshold_low_mag

    # </editor-fold>

    # <editor-fold desc="Group 5: Rate and frequency of water condition changes">
    def rate_and_frequency(self):
        """

        :return:
        """
        data_water = self.flow.data.groupby(pd.Grouper(freq=self.month_start[1]))
        rate_df = pd.DataFrame(columns=['Rise rate', 'Fall rate', 'Number of reversals'])
        boo = False
        mean = 0
        for type_rate in ['Rise rate', 'Fall rate']:
            for key, series in data_water:
                d1 = None
                values = []
                cont = 0
                for i in series.index:
                    if d1 is not None:
                        if self.check_rate(self.flow.data.loc[d1, self.station], self.flow.data.loc[i, self.station],
                                           type_rate):
                            boo = True
                            values.append(self.flow.data.loc[i, self.station] - self.flow.data.loc[d1, self.station])
                        else:
                            if boo:
                                mean = np.mean(values)
                                cont += 1
                                boo = False
                    d1 = i
                if boo:
                    mean = np.mean(values)
                    boo = False

                rate_df.at[key.year, type_rate] = mean
                if rate_df['Number of reversals'][key.year] > 0:
                    rate_df.at[key.year, 'Number of reversals'] = cont + rate_df['Number of reversals'][key.year]
                else:
                    rate_df.at[key.year, 'Number of reversals'] = cont
        return rate_df, self.metric_stats(rate_df, central_metric=self.central_metric,
                                          variation_metric=self.variation_metric)
    # </editor-fold>
