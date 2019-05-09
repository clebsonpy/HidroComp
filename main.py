import os

import pandas as pd
import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import timeit

from files.ons import Ons
from files.ana import Ana
from series.flow import Flow
from series.chuva import Chuva

if __name__ == '__main__':
    ini = timeit.default_timer()
    #file = "dadosXingo.csv"
    file = "/home/clebsonpy/Documents/Projetos/HydroComp/Medicoes/"
    #dados_chuva = Chuva(path=file, source='ANA', consistence=1)
    dados_vazao_obs = Flow(path=file, source='ANA', consistence=2)
    #dados_vazao_nat = Flow(path=file, source="ONS", station = "MANSO")
    #fig_nat = dados_vazao_nat.gantt()
    #fig_obs = dados_vazao_obs.gantt()
    #dados_chuva = dados_chuva.date(date_start="12/07/1981", date_end="31/12/1989")
    #dados_vazao_obs = dados_vazao_obs.date(date_start="12/07/1981", date_end="31/12/1989")
    #dados_vazao_nat = dados_vazao_nat.date(date_start="12/07/1981", date_end="31/12/1989")
    #dados = dados_chuva.data.combine_first(dados_vazao_nat.data)
    #dados = pd.DataFrame()
    #dados = dados.combine_first(dados_vazao_obs.data)
    #dados = dados.combine_first(dados_vazao_nat.data)
    #dados = Flow(dados)
    #fig = dados.gantt()
    #dados.to_csv("manso.csv")
    #print(dados_vazao)
    data, fig = dados_vazao_obs.plot_hydrogram()
    #dados = pd.read_csv(file, index_col=0, names=["Date", "XINGO"],
    #                    parse_dates=True)
    #flow = Flow(data=dados, source='ONS')
    #test = flow.date(date_start="01/01/1995", date_end="31/12/2012")

    #value_threshold = test.mean()['XINGO'] + test.std()['XINGO']
    #print(test.mean())
    #maximum = test.maximum(station='XINGO')
    #print(maximum.annual())
    #parcial = test.parcial(station="XINGO", type_criterion='median',
    #                       type_threshold="stationary", type_event="flood",
    #                       value_threshold=0.75, duration=0)
    #print(parcial.peaks)
    #print(parcial.test_autocorrelation())
    #data, fig = parcial.plot_hydrogram('Cheia')
    py.offline.plot(fig, filename='gráficos/hidrograma_manso_obs.html')

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
