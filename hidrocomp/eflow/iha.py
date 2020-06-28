from typing import Union, Type

from hidrocomp.eflow.exceptions import *
import pandas as pd
import calendar as cal
from hidrocomp.eflow.aspect import Magnitude, MagnitudeDuration, TimingExtreme, FrequencyDuration, RateFrequency
from hidrocomp.eflow.dhram import Dhram


class IHA:

    def __init__(self, flow, date_start: str = None, date_end: str = None, statistic="no-parametric",
                 central_metric="mean", variation_metric: str = "std", type_threshold="stationary", status=None,
                 month_water: int = None, type_criterion: str = None, threshold_high: float = None,
                 threshold_low: float = None, **kwargs):
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
        self.aspects = {"Magnitude": Union[Magnitude], "Magnitude and Duration": Union[MagnitudeDuration],
                        "Timing Extreme": Union[TimingExtreme], "Frequency and Duration": Union[FrequencyDuration],
                        "Rate and Frequency": Union[RateFrequency]}

        self.flow = flow
        self.status = status
        self._dhram = None
        self.month_start = self.get_month_start(month_water)
        self.date_start = pd.to_datetime(date_start, dayfirst=True)
        self.date_end = pd.to_datetime(date_end, dayfirst=True)
        self.statistic = statistic
        self.central_metric = central_metric
        self.variation_metric = variation_metric
        self.type_threshold = type_threshold
        self.type_criterion = type_criterion
        self.threshold_high = threshold_high
        self.threshold_low = threshold_low
        self.kwargs = kwargs

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

    def rva(self):
        pass

    def dhram(self, iha_obs, m: int = 500, interval: int = 95) -> Dhram:
        if self.status == "pos":
            raise StatusError("Dhram not available for self object!")
        if iha_obs.status == "pre":
            raise StatusError(f"status of {iha_obs} invalid!")

        self._dhram = Dhram()
        self._dhram.aspects = self.magnitude.dhram(aspect_pos=iha_obs.magnitude, m=m, interval=interval)
        self._dhram.aspects = self.magnitude_and_duration.dhram(aspect_pos=iha_obs.magnitude_and_duration, m=m,
                                                                interval=interval)
        self._dhram.aspects = self.timing_extreme.dhram(aspect_pos=iha_obs.timing_extreme, m=m, interval=interval)
        self._dhram.aspects = self.frequency_and_duration.dhram(aspect_pos=iha_obs.frequency_and_duration, m=m,
                                                                interval=interval)
        self._dhram.aspects = self.rate_and_frequency.dhram(aspect_pos=iha_obs.rate_and_frequency, interval=interval,
                                                            m=m)
        return self._dhram

    # <editor-fold desc="Group 1: Magnitude of monthly water conditions">
    @property
    def magnitude(self) -> Magnitude:
        if not isinstance(self.aspects["Magnitude"], Magnitude):
            magnit = Magnitude(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                               variation_metric=self.variation_metric, status=self.status)

            self.aspects["Magnitude"] = magnit
        return self.aspects["Magnitude"]

    # </editor-fold>

    # <editor-fold desc="Group 2: Magnitude and Duration of annual extreme water conditions">
    @property
    def magnitude_and_duration(self) -> MagnitudeDuration:
        if not isinstance(self.aspects["Magnitude and Duration"], MagnitudeDuration):
            magnit_and_durat = MagnitudeDuration(flow=self.flow, month_start=self.month_start, status=self.status,
                                                 central_metric=self.central_metric,
                                                 variation_metric=self.variation_metric)

            self.aspects["Magnitude and Duration"] = magnit_and_durat
        return self.aspects["Magnitude and Duration"]
    # </editor-fold>

    # <editor-fold desc="Group 3: Timing of annual extreme water conditions">
    @property
    def timing_extreme(self) -> TimingExtreme:
        if not isinstance(self.aspects["Timing Extreme"], TimingExtreme):
            timing = TimingExtreme(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                                   variation_metric=self.variation_metric, status=self.status)

            self.aspects["Timing Extreme"] = timing
        return self.aspects["Timing Extreme"]
    # </editor-fold>

    # <editor-fold desc="Group 4: Frequency and duration of high and low pulses">
    @property
    def frequency_and_duration(self) -> FrequencyDuration:
        if not isinstance(self.aspects["Frequency and Duration"], FrequencyDuration):
            freq = FrequencyDuration(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                                     variation_metric=self.variation_metric, status=self.status,
                                     type_threshold=self.type_threshold, type_criterion=self.type_criterion,
                                     threshold_high=self.threshold_high, threshold_low=self.threshold_low)

            self.aspects["Frequency and Duration"] = freq
        return self.aspects["Frequency and Duration"]
    # </editor-fold>

    # <editor-fold desc="Group 5: Rate and frequency of water condition changes">
    @property
    def rate_and_frequency(self) -> RateFrequency:
        if not isinstance(self.aspects["Rate and Frequency"], RateFrequency):
            rate = RateFrequency(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                                 variation_metric=self.variation_metric, status=self.status)

            self.aspects["Rate and Frequency"] = rate
        return self.aspects["Rate and Frequency"]
    # </editor-fold>

    @property
    def aspects_name(self) -> str:
        return f"Aspects_names({list(self.aspects.keys())})"
