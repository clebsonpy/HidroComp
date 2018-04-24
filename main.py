from data.vazao import Vazao
import timeit

if __name__ == '__main__':
    ini = timeit.default_timer()
    path = "/home/clebson/Documentos/Projetos/HidroComp1_8"
    serie_vazao = Vazao(path=path, font='ONS')

    print(serie_vazao.parcial('XINGO', 'stationary', 'cheia').threshold(value=0.75))


    fim = timeit.default_timer()
    print('Duração: ', fim-ini)
