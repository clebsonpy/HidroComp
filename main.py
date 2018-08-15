import os

import pandas as pd
import plotly as py
import timeit

from files.ons import Ons
from series.flow import Flow

if __name__ == '__main__':
    ini = timeit.default_timer()
    file = "/home/clebson/Documentos/Projetos/HidroComp1_8/dadosXingo.csv"
    dados = pd.read_csv(file, index_col=0, names=["Date", "XINGO"],
                        parse_dates=True)
    value_threshold = dados.mean() - dados.std()
    flow = Flow(data=dados, source='ONS')
#    maximum = flow.maximum(station='XINGO')
    parcial = flow.parcial(station="XINGO", type_criterion="median",
                           type_threshold="events_by_year", type_event="flood",
                           value_threshold=1.65, duration=5)
    print(parcial.event_peaks())
    data, fig = parcial.plot_hydrogram('Cheia')
    py.offline.plot(fig, filename='gráficos/Cheia.html')

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
