from api_ana.serie_temporal import SerieTemporal
import plotly as py
from hydrocomp.series.flow import Flow
import pandas as pd

class Simulation:

    def __init__(self, data, mxt_flow):
        self.data = data
        self.mxt_flow = mxt_flow

    def flows(self, flow, env_flow):
        if env_flow >= flow:
            tvr_flow = flow
            turb_flow = 0
        elif 0 <= (flow-env_flow) < self.mxt_flow:
            tvr_flow = env_flow
            turb_flow = flow - env_flow
        else: #(flow - env_flow) > self.mxt_flow:
            tvr_flow = flow - self.mxt_flow
            turb_flow = self.mxt_flow

        return tvr_flow, turb_flow

    def rule_01(self):
        """
        - Natural com menor Qmax de 1 ano (2016-17)
        - Situação crítica para algumas espécies, mas que já foi suportada

        :param:
        :return:
        """
        maximum = self.data.maximum()
        peaks = maximum.peaks
        env_flow = peaks.min().values[0]
        idx = []
        values_tvr = []
        values_turb = []
        for i in self.data.data.index:
            values = self.flows(self.data.data.loc[i].values[0], env_flow)
            values_tvr.append(values[0])
            values_turb.append((values[1]))
            idx.append(i)
        return pd.DataFrame([pd.Series(data=values_tvr, index=idx, name="TVR-01"),
                             pd.Series(data=values_turb, index=idx, name="TURB-01"), self.data.data["Natural"]]).T

    def rule_02(self):
        """
        - ANA
        :return:
        """
        A = [1100, 1600, 2500, 4000, 1800, 1200, 1000, 900, 750, 700, 800, 900]
        B = [1100, 1600, 4000, 8000, 4000, 2000, 1200, 900, 750, 700, 800, 900]

        idx = []
        values_tvr = []
        values_turb = []
        env = "B"
        year = self.data.date_start.year
        env_flow = A
        for i in self.data.data.index:
            if i.year != year:
                if env == "A":
                    env_flow = B
                else:
                    env_flow = A
                values = self.flows(self.data.data.loc[i].values[0], env_flow[i.month - 1])
            else:
                env_flow = env_flow
                values = self.flows(self.data.data.loc[i].values[0], env_flow[i.month - 1])

            values_tvr.append(values[0])
            values_turb.append((values[1]))
            idx.append(i)
        return pd.DataFrame([pd.Series(data=values_tvr, index=idx, name="TVR-02"),
                             pd.Series(data=values_turb, index=idx, name="TURB-02"), self.data.data["Natural"]]).T

    def rule_03(self):
        """
        - DNAEE 02/1984
        - Estudos de viabilidades

        :return:
        """
        pass

    def rule_04(self):
        """
        - Q90
        - Estudos de viabilidades

        :return:
        """
        env_flow = self.data.quantile(0.1)
        idx = []
        values_tvr = []
        values_turb = []
        for i in self.data.data.index:
            values = self.flows(self.data.data.loc[i].values[0], env_flow[0])
            values_tvr.append(values[0])
            values_turb.append((values[1]))
            idx.append(i)
        return pd.DataFrame([pd.Series(data=values_tvr, index=idx, name="TVR-04"),
                             pd.Series(data=values_turb, index=idx, name="TURB-04"), self.data.data["Natural"]]).T


if __name__ == "__main__":
    file = "Medicoes/PIMENTAL.csv"
    data = pd.read_csv(file, ',', index_col=0, parse_dates=True)
    flow = Flow(data=data, source='ONS', station="PIMENTAL")
    flow.station = "Natural"
    flow.data = flow.data.rename(columns={"PIMENTAL": "Natural"})
    month = flow.month_start_year_hydrologic()
    date_start = flow.date_start.replace(day=1, month=month[2])
    date_end = flow.date_end.replace(day=28, month=month[2]-1)
    flow.date(date_start=date_start, date_end=date_end)

    simulation = Simulation(data=flow, mxt_flow=15000)
    #Q1 = simulation.rule_01()
    #Q2 = simulation.rule_02()
    #Q = Q1.combine_first(Q2)
    Q4 = simulation.rule_04()
    #Q = Q.combine_first(Q4)

    flow_sim = Flow(data=Q4)
    fig, data = flow_sim.hydrogram(title="Hidrograma")

    py.offline.plot(fig, filename='graficos/hidro_sim2.html')
