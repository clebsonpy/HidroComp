import pandas as pd
import numpy as np
import calendar
import datetime

import plotly as py
import plotly.graph_objs as go

class Gantt(object):

    def __init__(self, data):
        self.data = data

    def get_gantt(self, df, less, index):

        color = 0
        n = 1
        for j in less.index:
            df.set_value(index = index, col = 'Task', value = self.data.name)
            df.set_value(index = index, col = 'Description', value = self.data.name + ' - %s' % j)
            df.set_value(index = index, col = 'IndexCol', value = color)
            df.set_value(index = index, col = 'Start', value = less['Inicio'].loc[j])
            df.set_value(index = index, col = 'Finish', value = less['Fim'].loc[j])
            color += (100*n)
            n *= -1
            index+=1
        return df, index
