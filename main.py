import os

import pandas as pd
import plotly as py
from files.ons import Ons

import timeit

from series.flow import Flow

if __name__ == '__main__':
    ini = timeit.default_timer()
    file = "/home/clebson/Documentos/Projetos/HidroComp1_8/dadosXingo.csv"
    dados = pd.read_csv(file, index_col=0, names=["Date", "XINGO"],
                        parse_dates=True)
    flow = Flow(data=dados, source='ONS')
    maximum = flow.maximum(station='XINGO')
    parcial = flow.parcial(station="XINGO", type_criterion="median",
                           type_threshold="stationary", type_event="drought",
                           value_threshold=0.25, duration=5)
    print(parcial.event_peaks())
    data, fig = parcial.plot_hydrogram('Estiagem')
    py.offline.plot(fig, filename='gráficos/estiagem.html')

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
