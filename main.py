from data.vazao import Vazao

if __name__ == '__main__':
    path = "/home/clebson/Documentos/Projetos/HidroComp1_8"
    serie_vazao = Vazao(path, font='ONS')
    serie_vazao.date('1/1/2000', '31/12/2010')
    print(serie_vazao.data)
