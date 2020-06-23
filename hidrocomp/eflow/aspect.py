from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np
import calendar as cal
from hidrocomp.eflow.exceptions import *
from hidrocomp.eflow.rva import RVA
from hidrocomp.eflow.dhram import DhramVariable, DhramAspect


class Aspect(metaclass=ABCMeta):
    name = None

    def __init__(self, flow, month_start, central_metric, variation_metric, status):
        self.variables = None
        self._dhram = None
        self.flow = flow
        self.station = flow.station
        self.month_start = month_start
        self.central_metric = central_metric
        self.variation_metric = variation_metric
        self.status = status
        self.data = self._data()
        self.metrics = self.metric_stats()

    def variable(self, name=None):
        name = name.capitalize()
        if name is None:
            raise VariableError("Variable is None")
        else:
            try:
                if self.variables[name] is None:
                    if self.status == "pre":
                        self.variables[name] = PreVariable(data=self.data[name], value=self.metrics.loc[name],
                                                           name=name)
                    elif self.status == "pos":
                        self.variables[name] = PosVariable(data=self.data[name], value=self.metrics.loc[name],
                                                           name=name)
                    else:
                        raise StatusError("Status invalid!")
                return self.variables[name]
            except KeyError:
                raise VariableError("Variable invalid! Options: {}".format(self.variables.keys()))

    def metric_stats(self):
        if self.central_metric == 'mean':
            mean = pd.DataFrame(self.data.mean(), columns=['Means'])
        elif self.central_metric == 'median':
            mean = pd.DataFrame(self.data.median(), columns=['Means'])
        else:
            raise NotStatistic('Not exist statistic {}: use {} or {}'.format(self.central_metric, 'mean', 'median'),
                               line=40)
        if self.variation_metric == 'cv':
            cv = pd.DataFrame(self.data.std() / self.data.mean(), columns=['Coeff. of Var.'])
        elif self.variation_metric == 'std':
            cv = pd.DataFrame(self.data.std(), columns=['Coeff. of Var.'])
        else:
            raise NotStatistic('Not exist statistic {}: use {} or {}'.format(self.variation_metric, 'cv', 'std'),
                               line=46)

        stats = mean.combine_first(cv)
        stats = stats.reindex(self.variables)
        return stats

    @abstractmethod
    def _data(self):
        pass

    def rva_frequency(self, aspect_pos, statistic="non-parametric", boundaries=17):
        frequency_aspect = pd.DataFrame()
        if aspect_pos.status == "pos":
            for i in self.variables:
                frequency = self.variable(name=i).rva(aspect_pos.variable(name=i), statistic=statistic,
                                                      boundaries=boundaries).frequency_pos
                frequency_aspect = frequency_aspect.combine_first(frequency)
                frequency_aspect = frequency_aspect.reindex(self.variables)
            return frequency_aspect
        else:
            raise StatusError("")

    def rva_measure_hydrologic_alteration(self, aspect_pos, statistic="non-parametric", boundaries=17):
        measure_hydrologic_alteration = pd.DataFrame()
        if aspect_pos.status == "pos":
            for i in self.variables:
                mha = self.variable(name=i).rva(aspect_pos.variable(name=i), statistic=statistic,
                                                boundaries=boundaries).measure_hydrologic_alteration()
                measure_hydrologic_alteration = measure_hydrologic_alteration.combine_first(mha)
                measure_hydrologic_alteration = measure_hydrologic_alteration.reindex(self.variables)
            return measure_hydrologic_alteration
        else:
            raise StatusError("Aspect status must be pos")

    def dhram(self, aspect_pos, m: int, interval: int):
        if self._dhram is None:
            self._dhram = DhramAspect(name=self.name)
            if aspect_pos.status == "pos":
                for i in self.variables:
                    dhram_variable = self.variable(name=i).dhram(variable_pos=aspect_pos.variable(name=i), m=m,
                                                                 interval=interval)
                    self._dhram.variables = dhram_variable
            else:
                raise StatusError("Aspect status must be pos")
        return self._dhram


class Variable:

    def __init__(self, data, value, name):
        self.data = data
        self.value = value
        self.name = name


class PosVariable(Variable):
    pass


class PreVariable(Variable):

    _dhram: DhramVariable = None
    _rva: RVA = None

    def rva(self, variable_pos, statistic="non-parametric", boundaries=17) -> RVA:
        if self._rva is None:
            self._rva = RVA(variable_pre=self, variable_pos=variable_pos, boundaries=boundaries, statistic=statistic)
        return self._rva

    def dhram(self, variable_pos, m: int, interval: int) -> DhramVariable:
        if self._dhram is None:
            self._dhram = DhramVariable(variable_pre=self, variable_pos=variable_pos, m=m, interval=interval)
        return self._dhram


class Magnitude(Aspect):
    name = "Magnitude"

    def _data(self):
        self.variables = {'January': None, 'February': None, 'March': None, 'April': None, 'May': None, 'June': None,
                          'July': None, 'August': None, 'September': None, 'October': None, 'November': None,
                          'December': None}
        years = self.flow.data.groupby(pd.Grouper(freq=self.month_start[1]))
        data = pd.DataFrame(columns=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                     'September', 'October', 'November', 'December'])
        for year in years:
            aux = year[1].groupby(pd.Grouper(freq='M')).mean()
            df = pd.DataFrame({year[0].year: {
                cal.month_name[i.month]: aux[self.station][i] for i in aux[self.station].index}})

            data = data.combine_first(df.T)

        mean_months = data
        return mean_months


class MagnitudeDuration(Aspect):
    name = "Magnitude and Duration"

    def _data(self):
        self.variables = {"1-day minimum": None, "1-day maximum": None, "3-day minimum": None, "3-day maximum": None,
                          "7-day minimum": None, "7-day maximum": None, "30-day minimum": None, "30-day maximum": None,
                          "90-day minimum": None, "90-day maximum": None, "Number of zero days": None,
                          "Base flow index": None}

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

        dic_zero = {i[0].year: i[1].loc[i[1][self.station].values == 0].sum().values[0]
                    for i in self.flow.data.groupby(pd.Grouper(freq=self.month_start[1]))}
        serie_dict_zero = pd.Series(data=dic_zero, name='Number of zero days')
        serie_dict_zero.loc[serie_dict_zero.isnull()].value = 0
        magn_and_duration = aver_data.combine_first(pd.DataFrame(serie_dict_zero))
        return magn_and_duration


class TimingExtreme(Aspect):
    name = "Timing Extreme"

    def _data(self):
        self.variables = {"Date of minimum": None, "Date of maximum": None}

        day_julian_max = self.flow.data[self.station].groupby(
            pd.Grouper(freq=self.month_start[1])).idxmax().dropna(axis=0)
        day_julian_min = self.flow.data[self.station].groupby(
            pd.Grouper(freq=self.month_start[1])).idxmin().dropna(axis=0)

        df_day_julian_max = pd.DataFrame(list(map(int, pd.DatetimeIndex(day_julian_max.values).strftime("%j"))),
                                         index=day_julian_max.index.year,
                                         columns=["Date of maximum"])

        df_day_julian_min = pd.DataFrame(list(map(int, pd.DatetimeIndex(day_julian_min.values).strftime("%j"))),
                                         index=day_julian_min.index.year,
                                         columns=["Date of minimum"])

        # combine the dfs of days julian
        timing_extreme = df_day_julian_max.combine_first(df_day_julian_min)
        return timing_extreme


class FrequencyDuration(Aspect):
    name = "Frequency and Duration"

    def __init__(self, flow, month_start, central_metric, variation_metric, status, type_threshold, type_criterion,
                 threshold_high, threshold_low):
        self.type_threshold = type_threshold
        self.type_criterion = type_criterion
        self.threshold_high = threshold_high
        self.threshold_low = threshold_low
        super().__init__(flow=flow, month_start=month_start, central_metric=central_metric,
                         variation_metric=variation_metric, status=status)

    def _data(self):
        self.variables = {"High pulse count": None, "High pulse duration": None, "Low pulse count": None,
                          "Low pulse duration": None}

        def aux_frequency_and_duration(events):
            name = {'flood': 'High', 'drought': 'Low'}
            type_event = events.type_event

            group = pd.DataFrame(
                index=pd.date_range(events.obj.date_start, events.obj.date_end, freq=self.month_start[1]),
                columns=["{} pulse duration".format(name[type_event]),
                         '{} pulse count'.format(name[type_event])])

            if len(events.peaks) != 0:
                duration_pulse = pd.DataFrame(events.peaks.groupby(
                    pd.Grouper(freq=self.month_start[1])).Duration.mean()).rename(
                    columns={"Duration": '{} pulse duration'.format(name[type_event])})

                pulse = pd.DataFrame(events.peaks.resample(self.month_start[1]).count().Duration).rename(
                    columns={"Duration": '{} pulse count'.format(name[type_event])})

                group = group.combine_first(duration_pulse)
                group = group.combine_first(pulse)

            group = group.fillna(value={'{} pulse count'.format(name[type_event]): 0})
            threshold = pd.DataFrame(pd.Series(events.threshold, name="{} Pulse Threshold".format(name[type_event])))
            return group, threshold

        self.events_high = self.flow.parcial(type_threshold=self.type_threshold, type_event="flood",
                                             type_criterion=self.type_criterion, value_threshold=self.threshold_high)

        frequency_and_duration_high, threshold_high_mag = aux_frequency_and_duration(self.events_high)

        self.events_low = self.flow.parcial(type_event='drought', type_threshold=self.type_threshold,
                                            type_criterion=self.type_criterion, value_threshold=self.threshold_low)
        frequency_and_duration_low, threshold_low_mag = aux_frequency_and_duration(self.events_low)

        frequency_and_duration = frequency_and_duration_high.combine_first(frequency_and_duration_low)
        return frequency_and_duration


class RateFrequency(Aspect):
    name = "Rate and Frequency"

    # <editor-fold desc="Check type rate"
    @staticmethod
    def check_rate(value1, value2, type_rate):
        if type_rate == 'Rise rate':
            return value1 < value2
        elif type_rate == 'Fall rate':
            return value1 > value2
    # </editor-fold>

    def _data(self):
        self.variables = {"Rise rate": None, "Fall rate": None, "Number of reversals": None}

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

        return rate_df
