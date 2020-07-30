from unittest import TestCase
import pandas as pd
from hidrocomp.series import Flow


class TestFlowOneStation(TestCase):

    def test_get_data_from_ana_hydro(self):
        flow = Flow(station="49330000", source="ANA")
        print(flow)
        print(flow.station)
        print(flow.inf_stations)

    def test_get_data_from_ana_hydro_list(self):
        flow = Flow(station=["49330000", "49370000"], source="ANA")
        print(flow)
        print(flow.station)
        print(flow.inf_stations)

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

    def test_get_data_from_all(self):
        flow = Flow(source="ONS")
        print(flow)

    def test_hydrogram_partial(self):
        flow = Flow(station="49330000", source="ANA")
        print(flow)
        fig, data = flow.parcial(type_threshold="stationary", type_event="flood", type_criterion=None,
                                 value_threshold=500).hydrogram("Test")

    def test_hydrogram_by_year(self):
        flow = Flow(station="49330000", source="ANA")
        print(flow)
        fig, data = flow.hydrogram_year("Title")

    def test_hydrogram(self):
        flow = Flow(station="49330000", source="ANA")
        print(flow)
        fig, data = flow.hydrogram("Title")
