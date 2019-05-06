import pandas as pd
import numpy as np
import calendar
import datetime

import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF

class Gantt(object):

    def __init__(self, data):
        self.data = data

    def get_gantt(self, less_period):

        df = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Description', 'IndexCol'])
        cont = 0
        for i in self.data:
            color = 0
            n = 1
            for j in less_period.index:
                df.set_value(index = cont, col = 'Task', value = i)
                df.set_value(index = cont, col = 'Description', value = i + ' - %s' % j)
                df.set_value(index = cont, col = 'IndexCol', value = color)
                df.set_value(index = cont, col = 'Start', value = less_period['Inicio'].loc[j])
                df.set_value(index = cont, col = 'Finish', value = less_period['Fim'].loc[j])
                cont += 1
                color += (100*n)
                n *= -1
        return df

    def plot(self, less_period):
        dfGantt = self.get_gantt(less_period=less_period)
        fig = FF.create_gantt(dfGantt, colors = '#000000', group_tasks=True, title= "Eventos de Cheias")
        return fig
