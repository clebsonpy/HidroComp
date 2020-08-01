from unittest import TestCase

import pandas as pd
import plotly.offline as pyo

from hidrocomp.series import Flow


class TestFlowOneStation(TestCase):
    flow_sar = Flow(data=pd.read_csv("E:\\Projetos\\HidroComp\\Artigo-Cha\\sar.csv", index_col=0, parse_dates=True))
    flow_ons = Flow(data=pd.read_csv("E:\\Projetos\\HidroComp\\Artigo-Cha\\ons.csv", index_col=0, parse_dates=True))
    flow_ana = Flow(data=pd.read_csv("E:\\Projetos\\HidroComp\\Artigo-Cha\\ana.csv", index_col=0, parse_dates=True))

    @staticmethod
    def interpolation(flow_sar, flow_ana):
        nulls = flow_sar.data["D19086"].isnull()
        date_start = flow_sar.data.loc[nulls].index[0] - pd.timedelta_range(start='1 day', periods=1, freq='D')
        date_end = flow_sar.data.loc[nulls].index[-1]

        date_range = pd.date_range(start=date_start.values[0], end=date_end)

        delta = None
        for date in date_range:
            if nulls[date]:
                flow_sar.data["D19086"][date] = flow_ana.data["66231000"][date] + delta
            delta = flow_sar.data["D19086"][date] - flow_ana.data["66231000"][date]

        return flow_sar

    @staticmethod
    def del_zeros(flow_sar, flow_ana):
        zeros = flow_sar.data.loc[flow_sar.data["D19086"] == 0].index

        for date in zeros:
            flow_sar.data["D19086"][date] = flow_ana.data["66231000"][date]

        return flow_sar

    def test_cha_graphics(self):
        start_period = "01/09/2003"
        end_period = "31/08/2018"
        flow_pre = Flow(data=self.flow_ons.data)
        flow_pre.date(date_start=start_period, date_end=end_period)
        threshold_high = flow_pre.quantile(0.75)[0]
        threshold_low = flow_pre.quantile(0.25)[0]

        names = {"1-day maximum": "1-day", "Date of maximum": "Date", "High events count": "Count",
                 "High events duration": "Duration", "1-day minimum": "1-day", "Date of minimum": "Date",
                 "Low events count": "Count", "Low events duration": "Duration"}

        iha_pre = flow_pre.iha(status='pre', statistic="no-parametric", central_metric="mean", month_water=9,
                               variation_metric="std", type_threshold="stationary", type_criterion="wrc",
                               threshold_high=threshold_high, threshold_low=threshold_low,
                               duration=1, aspects=["Magnitude and Duration", "Frequency and Duration",
                                                    "Timing Extreme"],
                               magnitude_and_duration=["1-day maximum", "1-day minimum"],
                               timing=["Date of maximum", "Date of minimum"])

        flow_pos = Flow(data=self.flow_sar.data["D19086"].to_frame())
        flow_pos.date(date_start=start_period, date_end=end_period)
        flow_pos = self.interpolation(flow_pos, self.flow_ana)
        flow_pos = self.del_zeros(flow_pos, self.flow_ana)
        iha_pos = flow_pos.iha(status='pos', statistic="no-parametric", central_metric="mean", month_water=9,
                               variation_metric="std", type_threshold="stationary", type_criterion="wrc",
                               threshold_high=threshold_high, threshold_low=threshold_low,
                               duration=1, aspects=["Magnitude and Duration", "Frequency and Duration",
                                                    "Timing Extreme"],
                               magnitude_and_duration=["1-day maximum", "1-day minimum"],
                               timing=["Date of maximum", "Date of minimum"])

        era = iha_pre.era(iha_obs=iha_pos)
        print(era.values_mean())
        print(era.values_std())
        fig, data = era.plot(by_type_events="Low", showlegend=True, names_variables=names)
        pyo.plot(fig, filename="../figs/test_cha.html")
