from data.vazao import Vazao

if __name__ == '__main__':
    path = "/home/clebson/Documentos/Projetos/HidroComp1_8"
    serie_vazao = Vazao(path, font='ONS')
    serie_vazao.month_start_year_hydrologic('XINGO')
    print(serie_vazao.month_start_year_hydrologic)
