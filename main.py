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
    flow = Flow(data=dados, source='ONS')
    flow.date(date_start="01/01/1995", date_end="31/12/2012")
    value_threshold = flow.data.mean()['XINGO'] - flow.data.std()['XINGO']
#    maximum = flow.maximum(station='XINGO')
    parcial = flow.parcial(station="XINGO", type_criterion='duration',
                           type_threshold="events_by_year", type_event="flood",
                           value_threshold=1.65, duration=0)
    print(parcial.event_peaks())
    print(parcial.test_autocorrelation())
    data, fig = parcial.plot_hydrogram('Cheia')
    py.offline.plot(fig, filename='gráficos/Cheia.html')

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
