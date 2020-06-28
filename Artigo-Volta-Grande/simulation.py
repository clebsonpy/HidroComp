from api_ana.serie_temporal import SerieTemporal
import plotly as py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from hidrocomp.series.flow import Flow
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
        elif (flow - env_flow) >= self.mxt_flow:
            tvr_flow = flow - self.mxt_flow
            turb_flow = self.mxt_flow

        return tvr_flow, turb_flow, env_flow

    def rule_01(self):
        """
        - Natural com menor Qmax de 1 ano (2016-17)
        - Situação crítica para algumas espécies, mas que já foi suportada

        :param:
        :return: tuple(DataFrame(columns=[TVR, Turbine, Naturally]), DataFrame(columns=[TVR - Naturally hash]))
        """
        date_start = "01/09/2015"
        date_end = "31/08/2016"
        env_flow = Flow(data=self.data.data.copy())
        env_flow.date(date_start=date_start, date_end=date_end)
        idx = []
        values_tvr = []
        values_turb = []
        values_env_flow = []
        for i in self.data.data.index:
            if i.month < 9:
                year = 2016
            else:
                year = 2015
            env_idx = i.replace(year=year)

            values = self.flows(self.data.data.loc[i].values[0], env_flow.data.loc[env_idx].values[0])
            values_tvr.append(values[0])
            values_turb.append((values[1]))
            values_env_flow.append(values[2])
            idx.append(i)

        return pd.DataFrame([pd.Series(data=values_tvr, index=idx, name="TVR"),
                             pd.Series(data=values_turb, index=idx, name="Derivation channel"),
                             self.data.data["Natural"],
                             pd.Series(data=values_env_flow, index=idx, name="e-flow")]).T, \
               pd.DataFrame(pd.Series(data=values_tvr, index=idx, name="TVR - Naturally hash"))

    def rule_02(self, hydro_start="A"):
        """
        - ANA
        :return: tuple(DataFrame(columns=[TVR, Turbine, Naturally]), DataFrame(columns=[TVR - ANA]))
        """
        A = [1100, 1600, 2500, 4000, 1800, 1200, 1000, 900, 750, 700, 800, 900]
        B = [1100, 1600, 4000, 8000, 4000, 2000, 1200, 900, 750, 700, 800, 900]
        env = hydro_start
        if hydro_start == "A":
            env_flow = A
        elif hydro_start == "B":
            env_flow = B
        idx = []
        values_tvr = []
        values_turb = []
        values_env_flow = []
        year = self.data.date_start.year
        for i in self.data.data.index:
            if i.year != year:
                if env == "A":
                    env_flow = B
                    env = "B"
                else:
                    env_flow = A
                    env = "A"
                year = i.year
                values = self.flows(self.data.data.loc[i].values[0], env_flow[i.month - 1])
            else:
                values = self.flows(self.data.data.loc[i].values[0], env_flow[i.month - 1])

            values_tvr.append(values[0])
            values_turb.append((values[1]))
            values_env_flow.append(values[2])
            idx.append(i)

        return pd.DataFrame([pd.Series(data=values_tvr, index=idx, name="TVR"),
                             pd.Series(data=values_turb, index=idx, name="Derivation channel"),
                             self.data.data["Natural"],
                             pd.Series(data=values_env_flow, index=idx, name="e-flow")]).T, \
               pd.DataFrame(pd.Series(data=values_tvr, index=idx, name="TVR - ANA"))

    def rule_03(self):
        """
        - DNAEE 02/1984
        - Estudos de viabilidades, 80% da menor vazão de no mínumo 10 anos de dados

        :return:tuple(DataFrame(columns=[TVR, Turbine, Naturally]), DataFrame(columns=[TVR - DNAEE]))
        """
        env_flow = self.data.data.groupby(pd.Grouper(freq="M")).mean().min() * 0.8

        idx = []
        values_tvr = []
        values_turb = []
        values_env_flow = []
        for i in self.data.data.index:
            values = self.flows(self.data.data.loc[i].values[0], env_flow[0])
            values_tvr.append(values[0])
            values_turb.append((values[1]))
            values_env_flow.append(values[2])
            idx.append(i)

        return pd.DataFrame([pd.Series(data=values_tvr, index=idx, name="TVR"),
                             pd.Series(data=values_turb, index=idx, name="Derivation channel"),
                             self.data.data["Natural"],
                             pd.Series(data=values_env_flow, index=idx, name="e-flow")]).T, \
               pd.DataFrame(pd.Series(data=values_tvr, index=idx, name="TVR - DNAEE"))

    def rule_04(self):
        """
        - Q90
        - Estudos de viabilidades

        :return: tuple(DataFrame(columns=[TVR, Turbine, Naturally]), DataFrame(columns=[TVR - 90Q]))
        """
        env_flow = self.data.quantile(0.1)
        idx = []
        values_tvr = []
        values_turb = []
        values_env_flow = []
        for i in self.data.data.index:
            values = self.flows(self.data.data.loc[i].values[0], env_flow[0])
            values_tvr.append(values[0])
            values_turb.append((values[1]))
            values_env_flow.append(values[2])
            idx.append(i)

        return pd.DataFrame([pd.Series(data=values_tvr, index=idx, name="TVR"),
                             pd.Series(data=values_turb, index=idx, name="Derivation channel"),
                             self.data.data["Natural"],
                             pd.Series(data=values_env_flow, index=idx, name="e-flow")]).T, \
               pd.DataFrame(pd.Series(data=values_tvr, index=idx, name="TVR - 90Q"))


if __name__ == "__main__":
    file = "../Medicoes/PIMENTAL.csv"
    data = pd.read_csv(file, ',', index_col=0, parse_dates=True)
    flow = Flow(data=data, source='ONS', station="PIMENTAL")
    flow.station = "Natural"
    flow.data = flow.data.rename(columns={"PIMENTAL": "Natural"})
    month = flow.month_start_year_hydrologic()
    date_start = flow.date_start.replace(day=1, month=month[2])
    date_end = flow.date_end.replace(day=28, month=month[2]-1)
    flow.date(date_start=date_start, date_end=date_end)
    simulation = Simulation(data=flow, mxt_flow=13950)
    #Q1 = simulation.rule_01()[0]
    #Q2 = simulation.rule_02()[0]
    #Q = Q1.combine_first(Q2)
    Q3 = simulation.rule_03()[0]
    #Q4 = simulation.rule_04()[0]
    #Q = Q1.combine_first(Q4)

    flow_sim = Flow(data=Q3)
    print(flow_sim)
    print(flow_sim.power_energy(efficiency=92, hydraulic_head=87.5, gravity=9.32, station="Derivation channel"))
    print(flow_sim.power_energy(efficiency=92, hydraulic_head=11.4, gravity=9.32, station="TVR"))
    #flow_sim.date(date_start="01/09/2007", date_end="31/08/2008")
    fig, data = flow_sim.hydrogram(title="Hydrograph - 90Q scenery", x_title="Date",
                                   y_title="Flow (m³/s)", color={"Naturally": "#002e6f", "TVR": "#8b0000",
                                                                 "Derivation channel": "#000000"})

    py.offline.plot(fig, filename='../graficos/hydro_rule_01.html',) # image_height=900, image_width=900)
