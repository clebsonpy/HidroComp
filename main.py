import os

import plotly as py
import timeit
import pandas as pd
from hydrocomp.series.flow import Flow

if __name__ == '__main__':
    ini = timeit.default_timer()
    # Boa Fortuna
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Boa Fortuna'
    file = os.path.abspath(os.path.join(path, "vazoes_T_39770000.txt"))
    flow = Flow(path=file, source='ANA', station='39770000_FLU')
    figg = flow.gantt(name='Gantt')

    flow.date(date_start='01/01/1974', date_end='31/12/1988')
    flow.data.to_csv(os.path.join(path, 'dados/boa_fortuna_74_88.csv'))

    q90 = flow.data.quantile(0.1)
    figp, datap = flow.permanence_curve()
    fig_year, data3 = flow.hydrogram_year()

    flow = Flow(path=file, source='ANA', station='39770000_FLU')
    flow.date(date_start='01/01/1990', date_end='31/12/2009')
    flow.data.to_csv(os.path.join(path, 'dados/boa_fortuna_90_09.csv'))
    flow_1 = flow.simulation_withdraw(criterion='q90', rate=50, value=q90, months=[11, 12, 1, 2, 3, 4])
    flow_1.to_csv(os.path.join(path, 'dados/boa_fortuna_withdraw_50_11_4.csv'))
    flow_2 = flow.simulation_withdraw(criterion='q90', rate=70, value=q90, months=[11, 12, 1, 2, 3, 4])
    flow_2.to_csv(os.path.join(path, 'dados/boa_fortuna_withdraw_70_11_4.csv'))
    flow_3 = flow.simulation_withdraw(criterion='q90', rate=50, value=q90)
    flow_3.to_csv(os.path.join(path, 'dados/boa_fortuna_withdraw_50_all.csv'))
    flow_4 = flow.simulation_withdraw(criterion='q90', rate=70, value=q90)
    flow_4.to_csv(os.path.join(path, 'dados/boa_fortuna_withdraw_70_all.csv'))

    flow = Flow(data=flow.data.combine_first(flow_1).combine_first(flow_2).combine_first(flow_3).combine_first(flow_4))
    figh, data = flow.hydrogram()
    """

    #Cachoeira Morena
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Cach. Morena'
    file = os.path.abspath(os.path.join(path, "vazoes_T_16100000.txt"))
    flow = Flow(path=file, source='ANA', station='16100000_FLU')
    figg = flow.gantt(name='Gantt')

    flow_pre = Flow(path=file, source='ANA', station='16100000_FLU')
    flow_pre.date(date_start='1/11/1973', date_end='31/10/1986')
    flow_pre.data.rename(columns={'16100000_FLU': '16100000_PRE'}, inplace=True)
    flow_pre.station = '16100000_PRE'
    flow_pre.data.to_csv(os.path.join(path, 'dados/cach_morena_73_86_pre.csv'))
    fig_year, data3 = flow_pre.hydrogram_year()

    flow_pos = Flow(path=file, source='ANA', station='16100000_FLU')
    flow_pos.date(date_start='1/11/1993', date_end='31/10/2005')
    flow_pos.data.rename(columns={'16100000_FLU': '16100000_POS'}, inplace=True)
    flow_pos.station = '16100000_POS'
    flow_pos.data.to_csv(os.path.join(path, 'dados/cach_morena_93_05_pos.csv'))

    flow = Flow(data=flow.data.combine_first(flow_pre.data).combine_first(flow_pos.data))
    figh, data = flow.hydrogram()
    """

    #Raizama
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Raizama'
    file = os.path.abspath(os.path.join(path, "vazoes_T_66231000.txt"))
    flow = Flow(path=file, source='ANA', station='66231000_FLU')
    figg = flow.gantt(name='Gantt')


    flow_pre = Flow(path=file, source='ANA', station='66231000_FLU')
    flow_pre.date(date_start='01/08/1981', date_end='31/07/1990')
    flow_pre.data.rename(columns={'66231000_FLU': '66231000_PRE'}, inplace=True)
    flow_pre.station = '66231000_PRE'
    flow_pre.data.to_csv(os.path.join(path, 'dados/raizama_81_90_pre.csv'))
    fig_year, data3 = flow_pre.hydrogram_year()

    flow_pos = Flow(path=file, source='ANA', station='66231000_FLU')
    flow_pos.date(date_start='01/08/2000', date_end='31/07/2004')
    flow_pos.data.rename(columns={'66231000_FLU': '66231000_POS'}, inplace=True)
    flow_pos.station = '66231000_POS'
    flow_pos.data.to_csv(os.path.join(path, 'dados/raizama_00_04_pos.csv'))


    flow = Flow(data=flow.data.combine_first(flow_pre.data).combine_first(flow_pos.data))
    figh, data = flow.hydrogram()
    """

    #Rosário Oeste
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Rosário Oeste'
    file = os.path.abspath(os.path.join(path, "vazoes_T_66250001.txt"))
    flow = Flow(path=file, source='ANA', station='66250001_FLU')
    figg = flow.gantt(name='Gantt')

    flow_pre = Flow(path=file, source='ANA', station='66250001_FLU')
    flow_pre.date(date_start='01/08/1981', date_end='31/07/1990')
    flow_pre.data.rename(columns={'66250001_FLU': '66250001_PRE'}, inplace=True)
    flow_pre.station = '66250001_PRE'
    flow_pre.data.to_csv(os.path.join(path, 'dados/Rosário Oeste_81_90_pre.csv'))
    fig_year, data3 = flow_pre.hydrogram_year()

    flow_pos = Flow(path=file, source='ANA', station='66250001_FLU')
    flow_pos.date(date_start='01/08/2000', date_end='31/07/2007')
    flow_pos.data.rename(columns={'66250001_FLU': '66250001_POS'}, inplace=True)
    flow_pos.station = '66250001_POS'
    flow_pos.data.to_csv(os.path.join(path, 'dados/Rosário Oeste_00_04_pos.csv'))

    flow = Flow(data=flow.data.combine_first(flow_pre.data).combine_first(flow_pos.data))
    figh, data = flow.hydrogram()
    """

    #Xingó
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Xingó'

    file_nat = os.path.abspath(os.path.join(path, 'Xingo_Nat.csv'))
    dados_nat = pd.read_csv(file_nat, index_col=0, parse_dates=True)
    dados_nat.rename(columns={'Flow': "Natural"}, inplace=True)
    flow_nat = Flow(data=dados_nat, station='Natural')
    fig_year, data3 = flow_nat.hydrogram_year()
    flow_nat.date(date_start='01/09/1995', date_end='31/08/2008')
    flow_nat.data.to_csv(os.path.join(path, 'dados/Xingo_Nat.csv'))

    file_obs = os.path.abspath(os.path.join(path, 'Xingo_Obs.csv'))
    flow_obs = pd.read_csv(file_obs, index_col=0, parse_dates=True)
    flow_obs.rename(columns={'Flow': "Observada"}, inplace=True)
    flow_obs = Flow(data=flow_obs, station="Observada")
    flow_obs.date(date_start='01/09/1995', date_end='31/08/2008')
    flow_obs.data.to_csv(os.path.join(path, 'dados/Xingo_Obs.csv'))

    flow = Flow(data=flow_nat.data.combine_first(flow_obs.data))
    print(flow)
    figh, data = flow.hydrogram()
    """

    # Porto Primavera
    """
    path = '/home/clebsonpy/Dropbox/IHA_Dados/Dados/Porto Primavera'

    file_nat = os.path.abspath(os.path.join(path, 'porto_primavera_nat.csv'))
    dados_nat = pd.read_csv(file_nat, index_col=0, parse_dates=True)
    dados_nat.rename(columns={'P. PRIMAVERA': "Natural"}, inplace=True)
    flow_nat = Flow(data=dados_nat, station='Natural')
    fig_year, data3 = flow_nat.hydrogram_year()
    flow_nat.date(date_start='01/09/1998', date_end='31/08/2011')
    flow_nat.data.to_csv(os.path.join(path, 'dados/porto_primavera_nat.csv'))

    file_obs = os.path.abspath(os.path.join(path, 'porto_primavera_obs.csv'))
    dados_obs = pd.read_csv(file_obs, index_col=0, parse_dates=True)
    dados_obs.rename(columns={'Vazão Defluente Média (m³/s)': "Observada"}, inplace=True)
    flow_obs = Flow(data=dados_obs, station="Observada")
    flow_obs.date(date_start='01/09/1998', date_end='31/08/2011')
    flow_obs.data.to_csv(os.path.join(path, 'dados/porto_primavera_obs.csv'))

    flow = Flow(data=flow_nat.data.combine_first(flow_obs.data))
    figh, data = flow.hydrogram()
    """

    #flow.data.to_csv('/home/clebsonpy/Desktop/Dados/Porto Primavera/porto_primavera_nat.csv')

    #flow_withd.to_csv('/home/clebsonpy/Desktop/Dados/Boa Fortuna/boa_fortuna_withdraw_months_all.csv')
    #flow = Flow(data=flow.data.combine_first(flow_withd))
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
    #fig, data = parcial.plot_hydrogram('Parcial')
    #py.offline.plot(figg, filename=os.path.join(path, 'gráficos/gantt.html'))
    py.offline.plot(fig_year, filename=os.path.join(path, 'gráficos/hidrograma_year.html'))
    py.offline.plot(figh, filename=os.path.join(path, 'gráficos/hidrograma.html'))
    #py.offline.plot(figp, filename=os.path.join(path, 'gráficos/permanência.html'))

    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
