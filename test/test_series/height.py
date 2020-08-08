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
