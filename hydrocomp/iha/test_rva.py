from unittest import TestCase
import pandas as pd
import os
from hydrocomp.iha.iha import IHA


class TestRVA(TestCase):

    path = os.path.abspath(os.path.join('Medicoes', 'dadosXingo_obs.csv'))
    data = pd.read_csv(path, ',', index_col=0, parse_dates=True)

    iha_obj_nat = IHA(data, month_water=1, status='pre', statistic='non-parametric', central_metric='mean',
                      variation_metric='cv',  type_criterion=None, type_threshold="stationary", duration=0,
                      threshold_high=4813, threshold_low=569.5, source='ONS', station='NAT')

    iha_obj_obs = IHA(data, month_water=1, status='pos', statistic='non-parametric', central_metric='mean',
                      variation_metric='cv', type_criterion=None, type_threshold="stationary", duration=0,
                      threshold_high=4813, threshold_low=569.5, source='CHESF', station='OBS')

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
        data_group_nat, data_nat = self.iha_obj_nat.magnitude()
        data_group_obs, data_obs = self.iha_obj_obs.magnitude()
        print(data_nat)
        print(data_obs)
        print(self.iha_obj_nat.rva(self.iha_obj_obs, group_iha='group1')[1])

    def test_moving_averages(self):
        data_group_nat, data_nat = self.iha_obj_nat.magnitude_and_duration()
        data_group_obs, data_obs = self.iha_obj_obs.magnitude_and_duration()
        print(data_nat)
        print(data_obs)
        print(self.iha_obj_nat.rva(self.iha_obj_obs, group_iha='group2'))

    def test_days_julian(self):
        data_group_nat, data_nat = self.iha_obj_nat.timing_extreme()
        data_group_obs, data_obs = self.iha_obj_obs.timing_extreme()
        print(data_nat)
        print(data_obs)
        print(self.iha_obj_nat.rva(self.iha_obj_obs, group_iha='group3'))

    def test_pulse(self):
        data_group_nat, data_nat = self.iha_obj_nat.frequency_and_duration()
        data_group_obs, data_obs = self.iha_obj_obs.frequency_and_duration()
        print(data_nat)
        print(data_obs)
        print(self.iha_obj_nat.rva(self.iha_obj_obs, group_iha='group4'))

    def test_rise_fall(self):
        data_group_nat, data_nat = self.iha_obj_nat.rate_and_frequency()
        data_group_obs, data_obs = self.iha_obj_obs.rate_and_frequency()
        print(data_nat)
        print(data_obs)
        print(self.iha_obj_nat.rva(self.iha_obj_obs, group_iha='group5'))
