from api_ana.serie_temporal import SerieTemporal
from hydrocomp.series.flow import Flow
import pandas as pd

class Simulation:

    def __init__(self, data, mxt_flow):
        self.data = data
        self.mxt_flow = mxt_flow

    def flows(self, flow, env_flow):
        if env_flow > flow:
            tvr_flow = flow
            turb_flow = 0
        elif 0 < (flow-env_flow) < self.mxt_flow:
            tvr_flow = env_flow
            turb_flow = flow - env_flow
        else: #(flow - env_flow) > self.mxt_flow:
            tvr_flow = flow - self.mxt_flow
            turb_flow = self.mxt_flow

        return tvr_flow, turb_flow

    def rule_01(self):
        """
        - Natural com Qmax de 1 ano (1997-98)
        - Situação crítica para algumas espécies, mas que já foi suportada

        :param:
        :return:
        """
        maximum = self.data.maximum()
        peaks = maximum.peaks
        mag = maximum.magnitude(period_return=1.05, estimador='MML')
        print(mag)

    def rule_02(self):
        """
        - ANA
        :return:
        """
        pass

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
        pass


if __name__ == "__main__":
    params = {'codEstacao': '18850000', 'tipoDados': '3', 'nivelConsistencia': '1'}
    data = Flow(station='18850000', source='ANA')
    simulation = Simulation(data=data, mxt_flow=1500)
    simulation.rule_01()
