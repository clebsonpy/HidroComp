from unittest import TestCase
from hidrocomp.series import Rainfall
import plotly.offline as pyo


class TestRainfall(TestCase):

    def test_gantt(self):
        rainfall = Rainfall(station=['937032', '937031', '937010', '937006', '937004', '937002', '937000', '936026',
                                     '936009', '936007', '837036', '837024', '837019', '837015', '837009', '837002',
                                     '836053', '836041', '836032', '836031', '836029', '836019', '836011', '836002',
                                     '836000'],
                            source='ANA')
        fig, data = rainfall.gantt(title="Test")
        pyo.plot(fig, filename="../figs/gantt_rainfall.html")

    def test_monthly_cumulative(self):
        rainfall = Rainfall(station='00937032', source='ANA')
        monthly_cumulative = rainfall.monthly_cumulative()
        print(monthly_cumulative.events)
        fig = monthly_cumulative.plot(title='Precipitação acumulada mensal')
        pyo.plot(fig, filename="../figs/cumulative_rainfall.html")
