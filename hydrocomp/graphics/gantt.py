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
            df.at[index, 'Task'] = self.data.name
            df.at[index, 'Description'] = self.data.name + ' - %s' % j
            df.at[index, 'IndexCol'] = color
            df.at[index, 'Start'] = less['Start'].loc[j]
            df.at[index, 'Finish'] = less['Finish'].loc[j]

            color += (100 * n)
            n *= -1
            index += 1
        return df, index

    @staticmethod
    def get_spells(data_peaks):
        df_spells = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Description', 'IndexCol'])
        index = 0
        print(data_peaks)
        for i in data_peaks.index:
            df_spells.at[index, 'Task'] = i.year
            df_spells.at[index, 'Description'] = '%s - %s' % (i.year, index)
            df_spells.at[index, 'IndexCol'] = index
            start = data_peaks['Start'].loc[i]
            end = data_peaks['End'].loc[i]
            data_start = pd.to_datetime('%s/%s/%s' % (start.month, start.day, 1998))
            data_end = pd.to_datetime(
                '%s/%s/%s' % (end.month, end.day, 1998)) if end.year >= start.year else pd.to_datetime(
                '%s/%s/%s' % (end.month, end.day, 1999))

            df_spells.at[index, 'Start'] = data_start
            df_spells.at[index, 'Finish'] = data_end

            index += 1
        return df_spells, index
