import os

import plotly as py
import timeit
import pandas as pd
from hydrocomp.series.flow import Flow

if __name__ == '__main__':
    ini = timeit.default_timer()
    #gev = Gev(shape=-0.168462, loc=6286.926278, scale=1819.961392)
    #x = gev.rvs(1000)
    #serie = pd.Series(x)
    #serie.to_csv('simulada.csv')
    #file = os.path.abspath(os.path.join('/home/clebsonpy/Downloads', 'Vazões_Diárias_1931_2015.xls'))
    file = os.path.abspath(os.path.join('/home/clebsonpy/Desktop/Dados/Caracaraí', 'vazoes_T_14710000.txt'))
    flow = Flow(path=file, source='ANA', consistence=2, station='14710000_FLU')
    flow.date(date_start='01/02/1994', date_end='31/12/2007')
    flow.data.to_csv('caracarai.csv')
    print(flow.simulation_withdraw(criterion='q90', rate=50, month_start=8, month_end=2))
    #file2 = os.path.abspath()

    #print(dados)
    #dados.data.to_csv('cachoeira_morena.csv')
    #dados_chuva = Chuva(path=file, source='ANA', consistence=2)
    #dados_cota = Cota(path=file, source='ANA', consistence=2)
    #dados = pd.read_csv('rio_ibicui_consistido.csv', index_col=0, parse_dates=True)
    #dados_estacao = pd.DataFrame(pd.read_csv(file, index_col=0, parse_dates=True)['Área'].add_suffix('_FLU')).T
    #dados_admen = pd.DataFrame()
    #for i in dados:
    #    print(type(dados_estacao[i]['Área']))
    #    print(dados[i])
    #    dados_admen = dados_admen.combine_first(pd.DataFrame(dados[i]/dados_estacao[i]['Área']))
    #print(dados_admen)
    #dados_flow = Flow(data=dados_admen)
    #dados = Flow(path=file, source="ONS",  station='XINGO', consistence=2)

    #fig, data = boxplot.Boxplot(magn_resample=flow.data, name='Rio Pardo').plot()
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
    #print(dados)
    #fig = flow.gantt(name='Gantt')
    #fig2, data = flow.hydrogram()
    #dados.data.to_csv("rio_ibicui_consistido.csv")
    #print(dados['1993'])

    #dados = psd.read_csv(file, index_col=0, names=["Date", "XINGO"],
    #                    parse_dates=True)
    #flow = Flow(data=dados_nat, source='ONS')
    #test = dados.date(date_start="01/01/1995", date_end="31/12/2012")

    #value_threshold = test.mean()['XINGO'] + test.std()['XINGO']
    #print(test.mean())
    #maximum = test.maximum(station='MANSO')
    #print(maximum.dist_gev.mvs())
    #parcial = flow.parcial(station="XINGO", type_criterion='autocorrelation', type_threshold="stationary", type_event="flood",
    #                        value_threshold=0.75, duration=6)
    #print(parcial.peaks)
    #print(parcial.threshold)
    #print(parcial.test_autocorrelation())

    #flow.data.to_csv('caracarai.csv')
    #fig3, data3 = flow.hydrogram_year()
    #fig, data = parcial.plot_hydrogram('Parcial')
    #py.offline.plot(fig, filename='gráficos/gantt_caracarai.html')
    #py.offline.plot(fig2, filename='gráficos/hydro__caracarai.html')
    #py.offline.plot(fig3, filename='gráficos/hydro_year_caracarai.html')

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
