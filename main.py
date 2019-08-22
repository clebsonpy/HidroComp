import os

import pandas as pd
import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import timeit

from files.ons import Ons
from files.ana import Ana
from series.flow import Flow
from series.rainfall import Chuva
from series.cota import Cota
from series.series_biuld import SeriesBiuld
from statistic.genextre import Gev

if __name__ == '__main__':
    ini = timeit.default_timer()
    #gev = Gev(shape=-0.168462, loc=6286.926278, scale=1819.961392)
    #x = gev.rvs(1000)
    #serie = pd.Series(x)
    #serie.to_csv('simulada.csv')

    #file = os.path.abspath(os.path.join('Medicoes', 'Ana'))
    file2 = os.path.abspath(os.path.join('Medicoes', 'dadosXingo.csv'))
    #dados_flow = Flow(path=file, source='ANA', consistence=2)
    #dados_chuva = Chuva(path=file, source='ANA', consistence=2)
    #dados_cota = Cota(path=file, source='ANA', consistence=2)
    dados_nat = pd.read_csv(file2, index_col=0, parse_dates=True)

    #dados = Flow(path=file, source="ONS")


    #fig_nat = dados_vazao_nat.gantt()
    #fig_obs = dados_vazao_obs.gantt()
    #dados_chuva = dados_chuva.date(date_start="12/07/1981", date_end="31/12/1989")
    #dados_vazao_nat = dados_vazao_nat.date(date_start="12/07/1981", date_end="31/12/1989")
    #dados_vazao_obs = dados_vazao_obs.date(date_start="12/07/1981", date_end="31/12/1989")
    #dados = dados_chuva.data.combine_first(dados_vazao_nat.data)
    #dados = pd.DataFrame()
    #dados = dados.combine_first(dados_chuva.data)
    #dados = dados.combine_first(dados_flow.data)
    #dados = dados.combine_first(dados_cota.data)
    #dados = dados.combine_first(dados_nat)
    #dados.rename(index=str, columns={"49330000_COT": "Cota", "49330000_FLU": "Flu_obs", "937023_PLU": "Precipitacao"}, inplace=True)
    #dados = Flow(dados_nat)
    #print(dados)
    #print(dados['2013'].get_month(8))
    #fig = dados.gantt(name = 'Gantt')
    #dados.data.to_csv("rsf_xingo.csv")
    #print(dados['1993'])
    #fig, data = dados.plot_hydrogram()
    #dados = psd.read_csv(file, index_col=0, names=["Date", "XINGO"],
    #                    parse_dates=True)
    flow = Flow(data=dados_nat, source='ONS')
    #test = dados.date(date_start="01/01/1995", date_end="31/12/2012")

    #value_threshold = test.mean()['XINGO'] + test.std()['XINGO']
    #print(test.mean())
    #maximum = test.maximum(station='MANSO')
    #print(maximum.dist_gev.mvs())
    parcial = flow.parcial(station="XINGO", type_criterion='autocorrelation', type_threshold="stationary", type_event="flood",
                            value_threshold=0.75, duration=6)
    #print(parcial.peaks)
    #print(parcial.threshold)
    #print(parcial.test_autocorrelation())
    #fig = dados.gantt("Xingó")
    fig, data = parcial.plot_hydrogram('Parcial')
    py.offline.plot(fig, filename='gráficos/parcial2.html')

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
