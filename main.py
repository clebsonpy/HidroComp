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
from series.series_biuld import SeriesBiuld
from test_statistic import TestGev

if __name__ == '__main__':
    ini = timeit.default_timer()
    file = "/home/clebsonpy/Documents/Projetos/HydroComp/Medicoes/dadosXingo.csv"
    #file2 = "/home/clebsonpy/Documentos/Projetos/HydroComp/Medicoes"
    #dados = Flow(path=file, source='ANA', consistence=2)
    dados = pd.read_csv(file, index_col=0, names=["Date", "XINGO"], parse_dates=True)

    #dados = Flow(path=file, source="ONS")
    #dados_chuva = Chuva(path=file2, source='ANA', consistence=1)
    #dados.rename(index=str, columns={"1455008": "COIMBRA_P", "66210000": "MANSO_JUS", "66231000": "COIMBRA_F"}, inplace=True)
    #fig_nat = dados_vazao_nat.gantt()
    #fig_obs = dados_vazao_obs.gantt()
    #dados_chuva = dados_chuva.date(date_start="12/07/1981", date_end="31/12/1989")
    #dados_vazao_nat = dados_vazao_nat.date(date_start="12/07/1981", date_end="31/12/1989")
    #dados_vazao_obs = dados_vazao_obs.date(date_start="12/07/1981", date_end="31/12/1989")
    #dados = dados_chuva.data.combine_first(dados_vazao_nat.data)
    #dados = pd.DataFrame()
    #dados = dados.combine_first(dados_chuva.data)
    #dados = dados.combine_first(dados_obs.data)
    #dados = dados.combine_first(dados_chuva.data)
    dados = Flow(dados)
    #print(dados)
    #print(dados['2013'].get_month(8))
    #fig = dados.gantt(name = 'Gantt')
    #dados.data.to_csv("barracao.csv")
    #print(dados['1993'])
    #fig, data = dados.plot_hydrogram()
    #dados = psd.read_csv(file, index_col=0, names=["Date", "XINGO"],
    #                    parse_dates=True)
    #flow = Flow(data=dados, source='ONS')
    test = dados.date(date_start="01/01/1995", date_end="31/12/2012")

    #value_threshold = test.mean()['XINGO'] + test.std()['XINGO']
    #print(test.mean())
    #maximum = test.maximum(station='MANSO')
    #print(maximum.dist_gev.mvs())
    parcial = dados.parcial(station="XINGO", type_criterion=None, type_threshold="stationary", type_event="flood",
                            value_threshold=4813, duration=0)
    #print(parcial.peaks)
    print(parcial.threshold)
    #print(parcial.test_autocorrelation())
    fig, data = parcial.plot_hydrogram('Cheia')
    #print(data)
    py.offline.plot(fig, filename='gráficos/hidroParcial.html')

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
