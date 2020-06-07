from hidrocomp.eflow.exceptions import *
import pandas as pd
import calendar as cal
from hidrocomp.eflow.aspect import Magnitude, MagnitudeDuration, TimingExtreme, FrequencyDuration, RateFrequency


class IHA:
    group = {
        'group1': 'magnitude',
        'group2': 'magnitude_and_duration',
        'group3': 'timing_extreme',
        'group4': 'frequency_and_duration',
        'group5': 'rate_and_frequency'
    }

    def __init__(self, flow, month_water=None, status=None, date_start=None, date_end=None,
                 statistic=None, central_metric=None, variation_metric=None, type_threshold=None, type_criterion=None,
                 threshold_high=None, threshold_low=None, **kwargs):
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
        ##self.source = kwargs['source']
        self.flow = flow #Flow(data, source=self.source, station=station)
        #self.station = self.get_station(station)
        self.status = status
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

    # <editor-fold desc="Group 1: Magnitude of monthly water conditions">
    def magnitude(self):
        return Magnitude(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                         variation_metric=self.variation_metric, status=self.status)

    # </editor-fold>

    # <editor-fold desc="Group 2: Magnitude and Duration of annual extreme water conditions">
    def magnitude_and_duration(self):
        return MagnitudeDuration(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                                 variation_metric=self.variation_metric, status=self.status)

    # </editor-fold>

    # <editor-fold desc="Group 3: Timing of annual extreme water conditions">

    def timing_extreme(self):
        return TimingExtreme(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                             variation_metric=self.variation_metric, status=self.status)

    # </editor-fold>

    # <editor-fold desc="Group 4: Frequency and duration of high and low pulses">
    def frequency_and_duration(self):
        return FrequencyDuration(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                                 variation_metric=self.variation_metric, status=self.status,
                                 type_threshold=self.type_threshold, type_criterion=self.type_criterion,
                                 threshold_high=self.threshold_high, threshold_low=self.threshold_low)

    # </editor-fold>

    # <editor-fold desc="Group 5: Rate and frequency of water condition changes">
    def rate_and_frequency(self):
        return RateFrequency(flow=self.flow, month_start=self.month_start, central_metric=self.central_metric,
                             variation_metric=self.variation_metric, status=self.status)
    # </editor-fold>
