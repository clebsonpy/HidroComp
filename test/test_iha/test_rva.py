from unittest import TestCase
import pandas as pd
import os
import plotly as py

from test.test_iha.simulation import Simulation
from hidrocomp.series.flow import Flow

class TestRVA(TestCase):
    file = "data/PIMENTAL.csv"
    data = pd.read_csv(file, ',', index_col=0, parse_dates=True)
    flow = Flow(data=data, source='ONS', station="PIMENTAL")
    flow.station = "Natural"
    flow.data = flow.data.rename(columns={"PIMENTAL": "Natural"})
    month = flow.month_start_year_hydrologic()
    date_start = flow.date_start.replace(day=1, month=month[2])  # date_start=01/03/1970
    date_end = flow.date_end.replace(day=31, month=month[0] - 1)  # date_end=31/08/2018
    flow.date(date_start=date_start, date_end=date_end)  # data range definition

    threshold_high = 11749.49
    threshold_low = 1397.0
    mxt_flow = 13950  # Maximum turbochargeable flow
    simulation = Simulation(data=flow, mxt_flow=mxt_flow)
    scenery_recovery_harsh = simulation.rule_01()

    date_start_del = pd.to_datetime("01/09/2015", dayfirst=True)
    date_end_del = pd.to_datetime("31/08/2016", dayfirst=True)
    data_del = pd.date_range(date_start_del, date_end_del, freq='D').values
    month_water = flow.month_start_year_hydrologic()[0]
    scenery_recovery_harsh_del = scenery_recovery_harsh[0].drop(data_del)
    data_tvr_scenery_recovery_harsh = Flow(data=pd.DataFrame(scenery_recovery_harsh_del.TVR))
    data_natural = Flow(data=pd.DataFrame(scenery_recovery_harsh_del.Natural))

    iha_obj_nat = data_natural.iha(month_water=1, status='pre', statistic='non-parametric', central_metric='mean',
                                   variation_metric='cv', type_criterion=None, type_threshold="stationary", duration=0,
                                   threshold_high=4813, threshold_low=569.5)

    iha_obj_obs = data_tvr_scenery_recovery_harsh.iha(month_water=1, status='pos', statistic='non-parametric',
                                                      central_metric='mean', variation_metric='cv', type_criterion=None,
                                                      type_threshold="stationary", duration=0, threshold_high=4813,
                                                      threshold_low=569.5)

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
        print(self.iha_obj_nat.summary())
        dhram = self.iha_obj_nat.dhram(iha_obs=self.iha_obj_obs, m=100, interval=95)
        print(self.iha_obj_nat.aspects_name)
        print(dhram.point)
        print(dhram.classification)
        fig, data = dhram.plot("mean")
        py.offline.plot(fig, filename=os.path.join("graficos", "dhram.html"))

        """
        magnitude_nat = self.iha_obj_nat.magnitude
        magnitude_obs = self.iha_obj_obs.magnitude
        print(magnitude_nat.metrics)
        print(magnitude_nat.metrics)
        print(magnitude_nat.rva_frequency(aspect_pos=magnitude_obs))
        print(magnitude_nat.rva_measure_hydrologic_alteration(aspect_pos=magnitude_obs))
        dhram = magnitude_nat.dhram(aspect_pos=magnitude_obs, m=1000, interval=95)
        print(dhram.abnormality)
        print(dhram.point)

        fig_std, data_std = dhram.variables["February"].plot(type="std")
        fig_mean, data_mean = dhram.variables["February"].plot(type="mean")

        py.offline.plot(fig_std, filename=os.path.join("graficos", "dhram_std.html"))
        py.offline.plot(fig_mean, filename=os.path.join("graficos", "dhram_mean.html"))
        """

    def test_moving_averages(self):
        magnitude_duration_nat = self.iha_obj_nat.magnitude_and_duration
        magnitude_duration_obs = self.iha_obj_obs.magnitude_and_duration
        print(magnitude_duration_nat.metrics)
        print(magnitude_duration_obs.metrics)
        print(magnitude_duration_nat.rva_frequency(aspect_pos=magnitude_duration_obs))
        print(magnitude_duration_nat.rva_measure_hydrologic_alteration(aspect_pos=magnitude_duration_obs))
        dhram = magnitude_duration_nat.dhram(aspect_pos=magnitude_duration_obs, m=100, interval=95)
        print(dhram.diff)
        print(dhram.point)

        #fig_std, data_std = dhram.variables["February"].plot(type="std")
        #fig_mean, data_mean = dhram.variables["February"].plot(type="mean")

        #py.offline.plot(fig_std, filename=os.path.join("graficos", "dhram_std.html"))
        #py.offline.plot(fig_mean, filename=os.path.join("graficos", "dhram_mean.html"))


    def test_days_julian(self):
        timing_extreme_nat = self.iha_obj_nat.timing_extreme
        timing_extreme_obs = self.iha_obj_obs.timing_extreme
        print(timing_extreme_nat.metrics)
        print(timing_extreme_obs.metrics)
        print(timing_extreme_nat.rva_frequency(aspect_pos=timing_extreme_obs))
        print(timing_extreme_nat.rva_measure_hydrologic_alteration(aspect_pos=timing_extreme_obs))
        dhram = timing_extreme_nat.dhram(aspect_pos=timing_extreme_obs, m=1000, interval=95)
        print(dhram.diff)
        print(dhram.point)


    def test_pulse(self):
        frequency_duration_nat = self.iha_obj_nat.frequency_and_duration
        frequency_duration_obs = self.iha_obj_obs.frequency_and_duration
        print(frequency_duration_nat.metrics)
        print(frequency_duration_obs.metrics)
        print(frequency_duration_nat.rva_frequency(aspect_pos=frequency_duration_obs))
        print(frequency_duration_nat.rva_measure_hydrologic_alteration(aspect_pos=frequency_duration_obs))
        dhram = frequency_duration_nat.dhram(aspect_pos=frequency_duration_obs, m=1000, interval=95)
        print(dhram.diff)
        print(dhram.point)

    def test_rise_fall(self):
        rate_and_frequency_nat = self.iha_obj_nat.rate_and_frequency
        rate_and_frequency_obs = self.iha_obj_obs.rate_and_frequency
        print(rate_and_frequency_nat.metrics)
        print(rate_and_frequency_obs.metrics)
        print(rate_and_frequency_nat.rva_frequency(aspect_pos=rate_and_frequency_obs))
        print(rate_and_frequency_nat.rva_measure_hydrologic_alteration(aspect_pos=rate_and_frequency_obs))
        dhram = rate_and_frequency_nat.dhram(aspect_pos=rate_and_frequency_obs, m=1000, interval=95)
        print(dhram.diff)
        print(dhram.point)
