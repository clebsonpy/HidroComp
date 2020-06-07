from unittest import TestCase
import pandas as pd
import os
from hidrocomp.eflow.iha import IHA
from hidrocomp.series.flow import Flow


class TestIHA(TestCase):

    path = os.path.abspath(os.path.join('data', 'dadosXingo_nat.csv'))
    data = pd.read_csv(path, ',', index_col=0, parse_dates=True)
    flow = Flow(data, source="ONS", station="XINGO")

    iha_obj_nat = IHA(flow, month_water=9, status='pre', statistic='non-parametric', central_metric='mean',
                      variation_metric='cv',  type_criterion=None, type_threshold="stationary", duration=0,
                      threshold_high=4813, threshold_low=569.5)

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
        magnitude = self.iha_obj_nat.magnitude()
        data2 = magnitude.metrics
        print(data)
        print(data2)
        self.test(data, data2)

    def test_moving_averages(self):
        data = self.read_iha('Group2.csv')
        magnitude_duration = self.iha_obj_nat.magnitude_and_duration()
        data2 = magnitude_duration.metrics
        print(data)
        print(data2)
        self.test(data, data2)

    def test_year_water(self):
        year_water = self.iha_obj_nat.get_month_start()
        self.assertEqual((9, 'AS-SEP', 3, 'AS-MAR'), year_water, 'Year Water: %s, %s, %s, %s' % (9, 'SEP', 3, 'AS-MAR'))

    def test_days_julian(self):
        data = self.read_iha('Group3.csv')
        timing_extreme = self.iha_obj_nat.timing_extreme()
        data2 = timing_extreme.metrics
        print(data)
        print(data2)
        self.test(data, data2)

    def test_pulse(self):
        data = self.read_iha('Group4.csv')
        frequency_duration = self.iha_obj_nat.frequency_and_duration()
        data2 = frequency_duration.metrics
        print(data)
        print(data2)
        self.test(data, data2)

    def test_rise_fall(self):
        data = self.read_iha('Group5.csv')
        rate_frequency = self.iha_obj_nat.rate_and_frequency()
        data2 = rate_frequency.metrics
        print(data)
        print(data2)
        self.test(data, data2)
