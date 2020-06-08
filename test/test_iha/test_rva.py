from unittest import TestCase
import pandas as pd
import os
from hidrocomp.eflow.iha import IHA
from hidrocomp.series.flow import Flow


class TestRVA(TestCase):

    path = os.path.abspath(os.path.join('data', 'dadosXingo_obs.csv'))
    data = pd.read_csv(path, ',', index_col=0, parse_dates=True)
    flow_nat = Flow(data.NAT, source="ONS", station="NAT")
    flow_obs = Flow(data.OBS, source="ONS", station="OBS")

    iha_obj_nat = IHA(flow_nat, month_water=1, status='pre', statistic='non-parametric', central_metric='mean',
                      variation_metric='cv',  type_criterion=None, type_threshold="stationary", duration=0,
                      threshold_high=4813, threshold_low=569.5)

    iha_obj_obs = IHA(flow_obs, month_water=1, status='pos', statistic='non-parametric', central_metric='mean',
                      variation_metric='cv', type_criterion=None, type_threshold="stationary", duration=0,
                      threshold_high=4813, threshold_low=569.5)

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
        magnitude_nat = self.iha_obj_nat.magnitude()
        magnitude_obs = self.iha_obj_obs.magnitude()
        print(magnitude_nat.metrics)
        print(magnitude_obs.metrics)
        print(magnitude_nat.rva_frequency(aspect_pos=magnitude_obs))
        print(magnitude_nat.rva_measure_hydrologic_alteration(aspect_pos=magnitude_obs))
        print(magnitude_nat.dhram_zscore(aspect_pos=magnitude_obs, n=1000, interval=95))
        print()

    def test_moving_averages(self):
        magnitude_duration_nat = self.iha_obj_nat.magnitude_and_duration()
        magnitude_duration_obs = self.iha_obj_obs.magnitude_and_duration()
        print(magnitude_duration_nat.metrics)
        print(magnitude_duration_obs.metrics)
        print(magnitude_duration_nat.rva_frequency(aspect_pos=magnitude_duration_obs))
        print(magnitude_duration_nat.rva_measure_hydrologic_alteration(aspect_pos=magnitude_duration_obs))
        print(magnitude_duration_nat.dhram_zscore(aspect_pos=magnitude_duration_obs, n=100, interval=95))

    def test_days_julian(self):
        timing_extreme_nat = self.iha_obj_nat.timing_extreme()
        timing_extreme_obs = self.iha_obj_obs.timing_extreme()
        print(timing_extreme_nat.metrics)
        print(timing_extreme_obs.metrics)
        print(timing_extreme_nat.rva_frequency(aspect_pos=timing_extreme_obs))
        print(timing_extreme_nat.rva_measure_hydrologic_alteration(aspect_pos=timing_extreme_obs))
        print(timing_extreme_nat.dhram_zscore(aspect_pos=timing_extreme_obs, n=100, interval=95))

    def test_pulse(self):
        frequency_duration_nat = self.iha_obj_nat.frequency_and_duration()
        frequency_duration_obs = self.iha_obj_obs.frequency_and_duration()
        print(frequency_duration_nat.metrics)
        print(frequency_duration_obs.metrics)
        print(frequency_duration_nat.rva_frequency(aspect_pos=frequency_duration_obs))
        print(frequency_duration_nat.rva_measure_hydrologic_alteration(aspect_pos=frequency_duration_obs))
        print(frequency_duration_nat.dhram_zscore(aspect_pos=frequency_duration_obs, n=100, interval=95))

    def test_rise_fall(self):
        rate_and_frequency_nat = self.iha_obj_nat.rate_and_frequency()
        rate_and_frequency_obs = self.iha_obj_obs.rate_and_frequency()
        print(rate_and_frequency_nat)
        print(rate_and_frequency_obs)
        print(rate_and_frequency_nat.rva_frequency(aspect_pos=rate_and_frequency_obs))
        print(rate_and_frequency_nat.rva_measure_hydrologic_alteration(aspect_pos=rate_and_frequency_obs))
        print(rate_and_frequency_nat.dhram_zscore(aspect_pos=rate_and_frequency_obs, n=100, interval=95))
