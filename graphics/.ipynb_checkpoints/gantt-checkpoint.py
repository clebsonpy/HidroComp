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
            df.at[index,'Task'] = self.data.name
            df.at[index,'Description'] = self.data.name + ' - %s' % j
            df.at[index,'IndexCol'] = color
            df.at[index,'Start'] = less['Inicio'].loc[j]
            df.at[index,'Finish'] = less['Fim'].loc[j]
                       
            color += (100*n)
            n *= -1
            index+=1
        return df, index
