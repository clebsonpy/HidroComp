from unittest import TestCase
from hidrocomp.series import Height
import plotly.offline as pyo


class TestHeight(TestCase):

    def test_gantt(self):
        height = Height(station=['49141000', '49153000', '49479000', '49480000', '49480001', '49490000', '49490001',
                                 '49490002', '49139000', '49168000', '49480050', '49510000', '49524000', '49525000',
                                 '49525001', '49530000', '39114500', '49369550', '49380000', '49384000', '39339120',
                                 '39339170', '49369500', '49369700', '49369800', '49371000', '49375000', '49330000'],
                        source='ANA')
        fig, data = height.gantt(title="Test")
        pyo.plot(fig, filename="../figs/gantt_height.html")

    def test_height_cotagram(self):
        height = Height(station='49330000', source='ANA')
        print(height)
        fig, data = height.cotagram(title="Test")
        pyo.plot(fig, filename="../figs/cotagram.html")

    def test_height_minimum(self):
        height = Height(station='49330000', source='ANA')
        minimum = height.minimum()
        print(minimum.peaks)
        fig, data = minimum.cotagram(title="Test", showlegend=True)
        pyo.plot(fig, filename="../figs/cotagram_minimum.html")

    def test_height_maximum(self):
        height = Height(station='49330000', source='ANA')
        maximum = height.maximum()
        print(maximum.peaks)
        fig, data = maximum.cotagram(title="Test", showlegend=True)
        pyo.plot(fig, filename="../figs/cotagram_maximum.html")

    def test_percentage_failures(self):
        height = Height(station='39770000', source='ANA')
        height.date(start_date='01/11/1976', end_date='30/09/2021')
        self.assertEqual(height.percentage_failures(), 0.005393148250291108)
        self.assertGreater(height.percentage_failures(), 0)
