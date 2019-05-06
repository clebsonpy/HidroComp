import os

import pandas as pd
import plotly as py
import plotly.graph_objs as go
import timeit

from files.ons import Ons
from files.ana import Ana
from series.flow import Flow
from series.chuva import Chuva

if __name__ == '__main__':
    ini = timeit.default_timer()
    #file = "dadosXingo.csv"
    file = "/home/clebsonpy/Documents/Projetos/HydroComp/Medicoes/"
    dados = Chuva(path=file, source='ANA')
    print(dados)
    #dados = dados.date(date_start="01/01/2010")
    #data, fig = dados.plot_hydrogram()
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
    #py.offline.plot(fig, filename='gráficos/Hidrograma.html')

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
