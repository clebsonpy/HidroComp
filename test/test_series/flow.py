from hidrocomp.series import Flow
from unittest import TestCase
import pandas as pd
import numpy as np
import os
from copy import copy
import plotly.offline as pyo


class TestFlow(TestCase):

    # flow = Flow(data=pd.read_csv("E:\\Projetos\\HidroComp\\Artigo-Cha\\ons.csv", index_col=0, parse_dates=True))
    flow = Flow(data=pd.read_csv("../../Medicoes/dadosXingo_nat.csv", index_col=0, parse_dates=True))
    print(os.path)

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
        print(flow.quantile(0.75))
        self.assertEqual(type(flow.quantile(0.75)), np.ndarray)
        print(flow.station)
        print(flow.inf_stations)

    def test_cal_month_flood_and_drought(self):
        flow = Flow(station="MANSO", source="ONS")
        self.assertEqual(flow.month_num_flood, 8)
        self.assertEqual(flow.month_num_drought, 2)
        self.assertEqual(flow.month_abr_flood, "AS-AUG")
        self.assertEqual(flow.month_abr_drought, "AS-FEB")
        self.assertEqual(type(flow.quantile(0.75)), np.float64)

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

        self.flow.date(start_date=start_period, end_date=end_period)
        partial = self.flow.partial(type_threshold="stationary", type_event="drought", type_criterion="autocorrelation",
                                    value_threshold=threshold_low, duration=1)

        fig, data = partial.plot_hydrogram(title="", threshold_line=True, point_start_end=False)
        pyo.plot(fig, filename="../figs/partial_high.html")

    def test_hydrogram_by_year(self):
        print(self.flow)
        fig, data = self.flow.hydrogram_year("Title", threshold=3600)
        pyo.plot(fig, filename="../figs/hidro_flow.html")

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

    def test_graphic_cumulative(self):
        flow = Flow(station='40740000', source='ANA')
        fig, data = flow.maximum().plot_distribution("", estimador="mml", type_function='cumulative')
        pyo.plot(fig, filename="../figs/cumulative_flow.html")

    def test_flow_min(self):
        self.flow.date(start_date="01/09/1995", end_date="31/08/2020")
        self.assertEqual(self.flow.flow_min("q95"), np.array([590.267]))

    def test_base_flow(self):
        self.flow.date(start_date="01/09/1995", end_date="31/08/2020")
        self.assertEqual(self.flow.base_flow(), 0.5029)

    def test_maximum(self):
        flow = Flow(station=['56110005', '56425000', '56430000', '56540001', '56610000', '56110005'], source='ANA')
        stations = flow.station
        maximum = {}
        for station in stations:
            aux = copy(flow)
            aux.station = station
            maximum[station] = aux.maximum()

        print(maximum['56110005'].peaks)
        print(maximum['56110005'].dist_gev.mml())

    def test_partial_flood_median(self):
        flow = Flow(station=['56110005', '56425000', '56430000', '56540001', '56610000', '56110005'], source='ANA')
        flow.station = '56110005'
        parti = flow.partial(events_type='flood', criterion_type='median', threshold_type='stationary',
                             threshold_value=0.75)
        print(parti.peaks)
        print(parti.dist_gpa.mml())

    def test_partial_flood_wrc(self):
        flow = Flow(station='XINGO', source='ONS')
        flow = flow.date(start_date="01/09/1931".format(self.flow.month_num_flood),
                         end_date="31/08/2018".format(self.flow.month_num_flood))
        partial = flow.partial(threshold_type="stationary", events_type="flood", criterion_type="wrc",
                               threshold_value=0.75, duration=5)

        # print(partial.peaks)
        print(partial.events)
        # dict_fig_partial, data_fig_partial = partial.plot_hydrogram(title="Eventos de duração parcial")
        # pyo.plot(dict_fig_partial, filename="../figs/hidro_flow.html")
        # print(partial.julian(start_events=True))
        # print(partial.julian_radius(start_events=False))
        print(len(partial.occurrence_dates_radius(start_day=15, start_month=1, end_day=31, end_month=5)))
        print(len(partial.occurrence_dates_radius(start_day=20, start_month=11, end_day=31, end_month=12)))

    def test_partial_drought_duration(self):
        flow = Flow(station='XINGO', source='ONS')
        parti = flow.partial(events_type='drought', criterion_type='duration', threshold_type='stationary',
                             threshold_value=0.25, duration=20)
        print(parti.peaks)

    def test_xingo(self):
        flow = Flow(station='XINGO', source='ONS')
        dict_fig, data_fig = flow.hydrogram(title='Hidrograma')
        pyo.plot(dict_fig, filename="../figs/hidro_flow.html")

    def test_monthly_average(self):
        flow = Flow(station='XINGO', source='ONS')
        monthly_average = flow.monthly_average()
        print(monthly_average.events)
        fig = monthly_average.plot(title='Média Mensal')
        pyo.plot(fig, filename="../figs/hidro_flow_monthly.html")

    def test_hydrogram_drought(self):
        # flow = Flow(station='XINGO', source='ONS')
        flow = self.flow.date(start_date="01/2/1988".format(self.flow.month_num_flood),
                              end_date="31/1/1989".format(self.flow.month_num_flood - 1))
        partial = flow.partial(events_type='drought', criterion_type='duration', threshold_type='stationary',
                               threshold_value=0.25, duration=20)

        dict_fig_partial, data_fig_partial = partial.plot_hydrogram(title="Eventos de duração parcial - Estiagem")
        pyo.plot(dict_fig_partial, filename="../figs/hidro_flow.html")

    def test_copy(self):
        flow = Flow(station=['XINGO', 'SALTO PILAO'], source='ONS')
        print(flow.__repr__())
        print(flow)
        flow_xingo = flow.copy(station='XINGO')
        print(flow_xingo.__repr__())
        print(flow_xingo)

    def test_percentage_failures(self):
        flow = Flow(station=['49330000'], source='ANA')
        flow.date(start_date='01/11/1976', end_date='30/09/2021')
        self.assertEqual(flow.percentage_failures(), 0.005393148250291108)

    def test_polar_with_duration(self):
        flow = Flow(station=['56110005', '56425000', '56430000', '56540001', '56610000', '56110005'], source='ANA')
        flow.station = '56110005'
        partial = flow.partial(events_type='flood', criterion_type='median', threshold_type='stationary',
                               threshold_value=0.75)

        fig, data = partial.plot_polar(title="", with_duration=True)
        pyo.plot(fig, filename="../figs/polar_duration.html")
