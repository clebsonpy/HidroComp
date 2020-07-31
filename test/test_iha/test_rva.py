from unittest import TestCase
import pandas as pd
import os
import plotly as py
from hidrocomp.series import Flow
from hidrocomp.series.partial import Partial


class TestRVA(TestCase):

    flow = Flow(station=["66231000", "66160000"], source="ANA")
    flow.date(date_start="01/09/2001", date_end="31/08/2008")

    alpha = 2.2458955
    data_mod = pd.DataFrame(flow.data["66160000"] * alpha)
    data_nat = Flow(data=data_mod)

    data_obs = Flow(data=pd.DataFrame(flow.data["66231000"]))

    # threshold_low = data.minimum().peaks.max().values[0]
    threshold_high = 1025
    threshold_low = 59
    duration = 1
    # duration = 10


    @staticmethod
    def read_iha(file):
        path = os.path.abspath(os.path.join('test_data', file))
        data = pd.read_csv(path, ';', index_col=0)
        return data

    def test(self, data, data2):
        for i in data.index:
            self.assertEqual(data.Means[i], data2.Means[i])
            self.assertEqual(data['Coeff. of Var.'][i], data2['Coeff. of Var.'][i])

    def test_mean_month(self):
        partial = self.data_nat.partial(type_criterion="autocorrelation", type_threshold="stationary",
                                        duration=self.duration, value_threshold=self.threshold_high, type_event="flood")

        fig, data = partial.plot_hydrogram("")
        py.offline.plot(fig, filename=os.path.join("graficos", "test.html"))

    def test_iha_events_high_pos(self):
        iha_pos = self.data_obs.iha(status='pos', statistic="no-parametric", central_metric="mean", month_water=9,
                               variation_metric="std", type_threshold="stationary",
                               threshold_high=self.threshold_high, threshold_low=self.threshold_low,
                               type_criterion="autocorrelation", duration=1,
                               aspects=["Magnitude and Duration", "Frequency and Duration", "Timing Extreme"],
                               magnitude_and_duration=["1-day maximum", "1-day minimum"],
                               timing=["Date of maximum", "Date of minimum"])

        partial = iha_pos.frequency_and_duration.events_high()

        fig, data = partial.plot_polar("")
        py.offline.plot(fig, filename=os.path.join("graficos", "test.html"))

    def test_iha_events_high_pre(self):
        iha_pre = self.data_nat.iha(status='pre', statistic="no-parametric", central_metric="mean", month_water=9,
                           variation_metric="std", type_threshold="stationary",
                           threshold_high=self.threshold_high, threshold_low=self.threshold_low, type_criterion="autocorrelation",
                           duration=1,
                           aspects=["Magnitude and Duration", "Frequency and Duration", "Timing Extreme"],
                           magnitude_and_duration=["1-day maximum", "1-day minimum"],
                           timing=["Date of maximum", "Date of minimum"])

        print(iha_pre.summary())

        partial = iha_pre.frequency_and_duration.events_high()

        fig, data = partial.plot_hydrogram("")
        py.offline.plot(fig, filename=os.path.join("graficos", "test.html"))


    def test_cha(self):
        iha_pre = self.data_nat.iha(status='pre', statistic="no-parametric", central_metric="mean", month_water=9,
                                    variation_metric="std", type_threshold="stationary", type_criterion="wrc",
                                    threshold_high=self.threshold_high, threshold_low=self.threshold_low,
                                    duration=self.duration)
        print(iha_pre)

        iha_pos = self.data_obs.iha(status='pos', statistic="no-parametric", central_metric="mean", month_water=9,
                                    variation_metric="std", type_threshold="stationary", type_criterion="wrc",
                                    threshold_high=self.threshold_high, threshold_low=self.threshold_low,
                                    duration=self.duration)

        cha = iha_pre.cha(iha_obs=iha_pos)
        fig, data = cha.plot(data_type="mean")
        py.offline.plot(fig, filename=os.path.join("graficos", "test.html"))

    def test_moving_averages(self):
        magnitude_duration_nat = self.iha_obj_nat.magnitude_and_duration
        magnitude_duration_obs = self.iha_obj_obs.magnitude_and_duration
        print(magnitude_duration_nat.metrics)
        print(magnitude_duration_obs.metrics)
        print(magnitude_duration_nat.rva_frequency(aspect_pos=magnitude_duration_obs))
        print(magnitude_duration_nat.rva_measure_hydrologic_alteration(aspect_pos=magnitude_duration_obs))
        dhram = magnitude_duration_nat.era(aspect_pos=magnitude_duration_obs, m=100, interval=95)
        print(dhram.diff)
        print(dhram.point)

    def test_days_julian(self):
        timing_extreme_nat = self.iha_obj_nat.timing_extreme
        timing_extreme_obs = self.iha_obj_obs.timing_extreme
        print(timing_extreme_nat.metrics)
        print(timing_extreme_obs.metrics)
        print(timing_extreme_nat.rva_frequency(aspect_pos=timing_extreme_obs))
        print(timing_extreme_nat.rva_measure_hydrologic_alteration(aspect_pos=timing_extreme_obs))
        dhram = timing_extreme_nat.era(aspect_pos=timing_extreme_obs, m=1000, interval=95)
        print(dhram.diff)
        print(dhram.point)

    def test_pulse(self):
        frequency_duration_nat = self.iha_obj_nat.frequency_and_duration
        frequency_duration_obs = self.iha_obj_obs.frequency_and_duration
        print(frequency_duration_nat.metrics)
        print(frequency_duration_obs.metrics)
        print(frequency_duration_nat.rva_frequency(aspect_pos=frequency_duration_obs))
        print(frequency_duration_nat.rva_measure_hydrologic_alteration(aspect_pos=frequency_duration_obs))
        dhram = frequency_duration_nat.era(aspect_pos=frequency_duration_obs, m=1000, interval=95)
        print(dhram.diff)
        print(dhram.point)

    def test_rise_fall(self):
        rate_and_frequency_nat = self.iha_obj_nat.rate_and_frequency
        rate_and_frequency_obs = self.iha_obj_obs.rate_and_frequency
        print(rate_and_frequency_nat.metrics)
        print(rate_and_frequency_obs.metrics)
        print(rate_and_frequency_nat.rva_frequency(aspect_pos=rate_and_frequency_obs))
        print(rate_and_frequency_nat.rva_measure_hydrologic_alteration(aspect_pos=rate_and_frequency_obs))
        dhram = rate_and_frequency_nat.era(aspect_pos=rate_and_frequency_obs, m=1000, interval=95)
        print(dhram.diff)
        print(dhram.point)
