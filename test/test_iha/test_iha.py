from unittest import TestCase
import pandas as pd
import os
from hydrocomp.iha.iha import IHA


class TestIHA(TestCase):

    path = os.path.abspath(os.path.join('data', 'dadosXingo_nat.csv'))
    data = pd.read_csv(path, ',', index_col=0, parse_dates=True)

    iha_obj_nat = IHA(data, month_water=9, status='pre', statistic='non-parametric', central_metric='mean',
                      variation_metric='cv',  type_criterion=None, type_threshold="stationary", duration=0,
                      threshold_high=4813, threshold_low=569.5, source='ONS', station='XINGO')

    @staticmethod
    def read_iha(file):
        path = os.path.abspath(os.path.join('data', file))
        data = pd.read_csv(path, ';', index_col=0)
        return data

    def test(self, data, data2):
        for i in data.index:
            erro_mean = abs(data.Means[i] - data2.Means[i])/data.Means[i]
            erro_cv = abs(data['Coeff. of Var.'][i] - data2['Coeff. of Var.'][i])/data['Coeff. of Var.'][i]
            self.assertLess(erro_mean, 0.08, msg="{} - {} - {}".format(i, erro_mean, "Mean"))
            self.assertLess(erro_cv, 0.08, msg="{} - {} - {}".format(i, erro_cv, "CV"))
            #self.assertEqual(data.Means[i], data2.Means[i])
            #self.assertEqual(data['Coeff. of Var.'][i], data2['Coeff. of Var.'][i], 7)

    def test_mean_month(self):
        data = self.read_iha('Group1.csv')
        data_group, data2 = self.iha_obj_nat.magnitude()
        print(data)
        print(data2)
        self.test(data, data2)

    def test_moving_averages(self):
        data = self.read_iha('Group2.csv')
        data_group, data2 = self.iha_obj_nat.magnitude_and_duration()
        print(data)
        print(data2)
        self.test(data, data2)

    def test_year_water(self):
        year_water = self.iha_obj_nat.get_month_start()
        self.assertEqual((9, 'AS-SEP', 3, 'AS-MAR'), year_water, 'Year Water: %s, %s, %s, %s' % (9, 'SEP', 3, 'AS-MAR'))

    def test_days_julian(self):
        data = self.read_iha('Group3.csv')
        data_group, data2 = self.iha_obj_nat.timing_extreme()
        print(data)
        print(data2)
        self.test(data, data2)

    def test_pulse(self):
        data = self.read_iha('Group4.csv')
        data_group, data2, partial_high_nat, partial_low_nat = self.iha_obj_nat.frequency_and_duration()
        print(data)
        print(data2)
        self.test(data, data2)

    def test_rise_fall(self):
        data = self.read_iha('Group5.csv')
        data_group, data2 = self.iha_obj_nat.rate_and_frequency()
        print(data)
        print(data2)
        self.test(data, data2)
