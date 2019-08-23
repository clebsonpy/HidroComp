from unittest import TestCase
import pandas as pd
import os
from iha.iha import IHA


class TestIHA(TestCase):

    path = os.path.abspath(os.path.join('Medicoes', 'dadosXingo.csv'))
    data = pd.read_csv(path, ',', index_col=0, parse_dates=True)
    iha_obj = IHA(data, month_water=1, status='pre', statistic='non-parametric', central_metric='mean',
                  variation_metric='cv',  type_criterion=None, type_threshold="stationary", duration=0,
                  threshold_high=4813, threshold_low=569.5)
    iha_obj_other = IHA(data, month_water=1, status='pos', statistic='non-parametric', central_metric='mean',
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
        data = self.read_iha('Group1.csv')
        data_group, data2 = self.iha_obj.magnitude()
        lower_line, median_line, upper_line = self.iha_obj.rva_line(data_group=data_group, boundaries=17)
        #rva_group = self.iha_obj.rva_frequency(data_group=data_group, lower_line=lower_line, upper_line=upper_line)
        print(self.iha_obj.rva(self.iha_obj_other, group_iha='group1'))
        self.test(data, data2)

    def test_moving_averages(self):
        data = self.read_iha('Group2.csv')
        data_group, data2 = self.iha_obj.magnitude_and_duration()
        lower_line, median_line, upper_line = self.iha_obj.rva_line(data_group=data_group, boundaries=17)
        print(self.iha_obj.rva_frequency(data_group=data_group, lower_line=lower_line, upper_line=upper_line))
        self.test(data, data2)

    def test_year_water(self):
        year_water = self.iha_obj.get_month_start()
        self.assertEqual((9, 'AS-SEP'), year_water, 'Year Water: %s, %s' % (9, 'SEP'))

    def test_days_julian(self):
        data_group, data2 = self.iha_obj.timing_extreme()
        data = self.read_iha('Group3.csv')
        lower_line, median_line, upper_line = self.iha_obj.rva_line(data_group=data_group, boundaries=17)
        print(self.iha_obj.rva_frequency(data_group=data_group, lower_line=lower_line, upper_line=upper_line))
        self.test(data, data2)

    def test_pulse(self):
        data_group, data2, threshold_high, threshold_low = self.iha_obj.frequency_and_duration()
        data = self.read_iha('Group4.csv')
        lower_line, median_line, upper_line = self.iha_obj.rva_line(data_group=data_group, boundaries=17)
        print(self.iha_obj.rva_frequency(data_group=data_group, lower_line=lower_line, upper_line=upper_line))
        self.test(data, data2)

    def test_rise_fall(self):
        data = self.read_iha('Group5.csv')
        data_group, data2 = self.iha_obj.rate_and_frequency()
        lower_line, median_line, upper_line = self.iha_obj.rva_line(data_group=data_group, boundaries=17)
        print(self.iha_obj.rva_frequency(data_group=data_group, lower_line=lower_line, upper_line=upper_line))
        self.test(data, data2)
