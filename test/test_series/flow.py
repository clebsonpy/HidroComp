from unittest import TestCase
import pandas as pd
from hidrocomp.series import Flow
import plotly.offline as pyo


class TestFlow(TestCase):

    # flow = Flow(data=pd.read_csv("E:\\Projetos\\HidroComp\\Artigo-Cha\\ons.csv", index_col=0, parse_dates=True))
    flow = Flow(data=pd.read_csv("E:\\Projetos\\HidroComp\\Medicoes\\dadosXingo_nat.csv", index_col=0, parse_dates=True))

    def test_get_data_from_ana_hydro(self):
        flow = Flow(station="49330000", source="ANA")
        print(flow)
        print(flow.station)
        print(flow.inf_stations)

    def test_get_data_from_ana_hydro_list(self):
        print(self.flow)
        print(self.flow.station)
        print(self.flow.inf_stations)

    def test_get_data_from_ana_sar(self):
        flow = Flow(station="19086", source="SAR")
        afluencia = [192.00, -68301.00, 68795.00, 382.00, 489.00, 719.00]
        defluencia = [78.00, 122.00, 95.00, 105.00, 173.00, 245.00]
        data_flow = {"A19086": afluencia, "D19086": defluencia}
        data = ["05/01/2002", "06/01/2002", "07/01/2002", "08/01/2002", "09/01/2002", "10/01/2002"]
        data = pd.to_datetime(data, dayfirst=True)
        data_obs = pd.DataFrame(index=data, data=data_flow)
        for i in data_obs.index:
            self.assertEqual(data_obs["A19086"][i], flow.data["A19086"][i])

    def test_get_data_from_ana_sar_list(self):
        flow = Flow(station=["19086", "19002"], source="SAR")
        print(flow)
        print(flow.station)
        print(flow.inf_stations)

    def test_cal_month_flood_and_drought(self):
        flow = Flow(station="MANSO", source="ONS")
        self.assertEqual(flow.month_num_flood, 8)
        self.assertEqual(flow.month_num_drought, 2)
        self.assertEqual(flow.month_abr_flood, "AS-AUG")
        self.assertEqual(flow.month_abr_drought, "AS-FEB")

    def test_define_month_start_year(self):
        flow = Flow(station="MANSO", source="ONS")
        flow.month_num_flood = 2
        self.assertEqual(flow.month_num_flood, 2)
        self.assertEqual(flow.month_num_drought, 8)
        self.assertEqual(flow.month_abr_flood, "AS-FEB")
        self.assertEqual(flow.month_abr_drought, "AS-AUG")

    def test_get_data_from_ons_all(self):
        flow = Flow(source="ONS")
        print(flow)

    def test_hydrogram_partial(self):
        start_period = "01/09/2003"
        end_period = "31/08/2018"
        threshold_high = 203
        threshold_low = 99

        self.flow.date(date_start=start_period, date_end=end_period)
        partial = self.flow.partial(type_threshold="stationary", type_event="drought", type_criterion="autocorrelation",
                                    value_threshold=threshold_low, duration=1)

        fig, data = partial.plot_hydrogram(title="", line_threshold=True, point_start_end=False)
        pyo.plot(fig, filename="../figs/partial_high.html")

    def test_hydrogram_by_year(self):
        print(self.flow)
        fig, data = self.flow.hydrogram_year("Title")

    def test_hydrogram(self):
        print(self.flow)
        fig, data = self.flow.hydrogram("Title")

    def test_rating_curve(self):
        fig, data = self.flow.rating_curve("Curva de Permanência")
        pyo.plot(fig, filename="../figs/rating.html")

    def test_gantt(self):
        flow = Flow(station=['49141000', '49153000', '49479000', '49480000', '49480001', '49490000', '49490001',
                             '49490002', '49139000', '49168000', '49480050', '49510000', '49524000', '49525000',
                             '49525001', '49530000', '39114500', '49369550', '49380000', '49384000', '39339120',
                             '39339170', '49369500', '49369700', '49369800', '49371000', '49375000', '49330000'],
                    source='ANA')
        fig, data = flow.gantt(title="Test")
        pyo.plot(fig, filename="../figs/gantt_flow.html")
