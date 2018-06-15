import os

import pandas as pd

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
    print(maximum.annual())
    parcial = flow.parcial(station="XINGO", type_criterion="median",
                           type_threshold="stationary", type_event="flood",
                           value_threshold=0.75, duration=5)
    print(parcial.event_peaks())

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
