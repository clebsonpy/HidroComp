from typing import Union

from hidrocomp.eflow.exceptions import *
import pandas as pd
import calendar as cal
from hidrocomp.eflow.aspect import Magnitude, MagnitudeDuration, TimingExtreme, FrequencyDuration, RateFrequency
from hidrocomp.eflow import Era, RVA


class IHA:

    aspects_all = {"Magnitude": Union[Magnitude], "Magnitude and Duration": Union[MagnitudeDuration],
                   "Timing Extreme": Union[TimingExtreme], "Frequency and Duration": Union[FrequencyDuration],
                   "Rate and Frequency": Union[RateFrequency]}

    def __init__(self, flow, date_start: str = None, date_end: str = None, statistic="no-parametric",
                 central_metric="mean", variation_metric: str = "std", type_threshold="stationary", status=None,
                 month_water: int = None, type_criterion: str = None, threshold_high: float = None,
                 threshold_low: float = None, aspects: list = None, magnitude: list = None,
                 magnitude_and_duration: list = None, timing: list = None, frequency_and_duration: list = None,
                 rate_and_frequency: list = None, new_iha: bool = False, **kwargs):
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

        if aspects is not None:
            self.aspects = {}
            for aspect in aspects:
                self.aspects[aspect] = self.aspects_all[aspect]
        else:
            self.aspects = self.aspects_all.copy()

        self.flow = flow
        self.status = status
        self._era = None
        self.month_start = self.get_month_start(month_water)
        self.date_start = pd.to_datetime(date_start, dayfirst=True)
        self.date_end = pd.to_datetime(date_end, dayfirst=True)
        self.statistic = statistic
        self.__events_high = None
        self.__events_low = None
        self.central_metric = central_metric
        self.variation_metric = variation_metric
        self.type_threshold = type_threshold
        self.type_criterion = type_criterion
        self.threshold_high = threshold_high
        self.threshold_low = threshold_low
        self.magnitude_variables = magnitude
        self.magnitude_and_duration_variables = magnitude_and_duration
        self.timing_extreme_variables = timing
        self.frequency_and_duration_variables = frequency_and_duration
        self.rate_and_frequency_variables = rate_and_frequency
        self.new_iha = new_iha
        self.kwargs = kwargs

    @property
    def events_high(self):
        if self.__events_high is None:
            self.__events_high = self.flow.partial(type_threshold=self.type_threshold, type_event="flood",
                                                   type_criterion=self.type_criterion,
                                                   value_threshold=self.threshold_high, **self.kwargs)
        return self.__events_high

    @property
    def events_low(self):
        if self.__events_low is None:
            self.__events_low = self.flow.partial(type_event='drought', type_threshold=self.type_threshold,
                                                  type_criterion=self.type_criterion,
                                                  value_threshold=self.threshold_low, **self.kwargs)
        return self.__events_low

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
            return self.flow.month_start_year_hydrologic()
        else:
            self.flow.month_abr = 'AS-%s' % cal.month_abbr[month_water].upper()
            self.flow.month_num = month_water
            return self.flow.month_num, self.flow.month_abr

    # </editor-fold>

    def __str__(self) -> str:
        return self.summary().__str__()

    def rva(self, iha_obs, boundaries) -> RVA:
        print(self.magnitude.variable("April"))
        rva = RVA(self.magnitude, iha_obs.magnitude, self.statistic, boundaries)
        return rva

    def era(self, iha_obs, m: int = 500, interval: int = 95) -> Era:
        if self.status == "pos":
            raise StatusError("Dhram not available for self object!")
        if iha_obs.status == "pre":
            raise StatusError(f"status of {iha_obs} invalid!")

        self._era = Era()
        for aspect in self.aspects:
            if aspect == "Magnitude":
                self._era.aspects = self.magnitude.era(aspect_pos=iha_obs.magnitude, m=m, interval=interval)
            elif aspect == "Magnitude and Duration":
                self._era.aspects = self.magnitude_and_duration.era(aspect_pos=iha_obs.magnitude_and_duration, m=m,
                                                                    interval=interval)
            elif aspect == "Timing Extreme":
                self._era.aspects = self.timing_extreme.era(aspect_pos=iha_obs.timing_extreme, m=m, interval=interval)
            elif aspect == "Frequency and Duration":
                self._era.aspects = self.frequency_and_duration.era(aspect_pos=iha_obs.frequency_and_duration, m=m,
                                                                    interval=interval)
            elif aspect == "Rate and Frequency":
                self._era.aspects = self.rate_and_frequency.era(aspect_pos=iha_obs.rate_and_frequency, m=m,
                                                                interval=interval)
        return self._era

    def summary(self):
        df = pd.DataFrame()
        idx = []
        for aspect in self.aspects:
            if aspect == "Magnitude":
                df = df.combine_first(self.magnitude.metrics)
                idx = idx + list(self.magnitude.variables.keys())
            elif aspect == "Magnitude and Duration":
                df = df.combine_first(self.magnitude_and_duration.metrics)
                idx = idx + list(self.magnitude_and_duration.variables.keys())
            elif aspect == "Timing Extreme":
                df = df.combine_first(self.timing_extreme.metrics)
                idx = idx + list(self.timing_extreme.variables.keys())
            elif aspect == "Frequency and Duration":
                df = df.combine_first(self.frequency_and_duration.metrics)
                idx = idx + list(self.frequency_and_duration.variables.keys())
            elif aspect == "Rate and Frequency":
                df = df.combine_first(self.rate_and_frequency.metrics)
                idx = idx + list(self.rate_and_frequency.variables.keys())
        return df.reindex(idx)

    # <editor-fold desc="Group 1: Magnitude of monthly water conditions">
    @property
    def magnitude(self) -> Magnitude:
        if not isinstance(self.aspects["Magnitude"], Magnitude):
            magnit = Magnitude(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                               variation_metric=self.variation_metric, status=self.status,
                               variables=self.magnitude_variables)

            self.aspects["Magnitude"] = magnit
        return self.aspects["Magnitude"]

    # </editor-fold>

    # <editor-fold desc="Group 2: Magnitude and Duration of annual extreme water conditions">
    @property
    def magnitude_and_duration(self) -> MagnitudeDuration:
        if not isinstance(self.aspects["Magnitude and Duration"], MagnitudeDuration):
            if self.new_iha:
                magnit_and_durat = MagnitudeDuration(flow=self.flow, month_start=self.month_start, status=self.status,
                                                     central_metric=self.central_metric, events_high=self.events_high,
                                                     events_low=self.events_low,
                                                     variables=self.magnitude_and_duration_variables,
                                                     variation_metric=self.variation_metric)
            else:
                magnit_and_durat = MagnitudeDuration(flow=self.flow, month_start=self.month_start, status=self.status,
                                                     central_metric=self.central_metric,
                                                     variables=self.magnitude_and_duration_variables,
                                                     variation_metric=self.variation_metric)
            self.aspects["Magnitude and Duration"] = magnit_and_durat
        return self.aspects["Magnitude and Duration"]
    # </editor-fold>

    # <editor-fold desc="Group 3: Timing of annual extreme water conditions">
    @property
    def timing_extreme(self) -> TimingExtreme:
        if not isinstance(self.aspects["Timing Extreme"], TimingExtreme):
            timing = TimingExtreme(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                                   variation_metric=self.variation_metric, status=self.status,
                                   events_high=self.events_high, events_low=self.events_low,
                                   variables=self.timing_extreme_variables)

            self.aspects["Timing Extreme"] = timing
        return self.aspects["Timing Extreme"]
    # </editor-fold>

    # <editor-fold desc="Group 4: Frequency and duration of high and low pulses">
    @property
    def frequency_and_duration(self) -> FrequencyDuration:
        if not isinstance(self.aspects["Frequency and Duration"], FrequencyDuration):
            freq = FrequencyDuration(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                                     variation_metric=self.variation_metric, status=self.status,
                                     events_high=self.events_high, events_low=self.events_low,
                                     variables=self.frequency_and_duration_variables, **self.kwargs)

            self.aspects["Frequency and Duration"] = freq
        return self.aspects["Frequency and Duration"]
    # </editor-fold>

    # <editor-fold desc="Group 5: Rate and frequency of water condition changes">
    @property
    def rate_and_frequency(self) -> RateFrequency:
        if not isinstance(self.aspects["Rate and Frequency"], RateFrequency):
            rate = RateFrequency(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                                 variation_metric=self.variation_metric, status=self.status,
                                 variables=self.rate_and_frequency_variables)

            self.aspects["Rate and Frequency"] = rate
        return self.aspects["Rate and Frequency"]
    # </editor-fold>

    @property
    def aspects_name(self) -> str:
        return f"Aspects_names({list(self.aspects.keys())})"
