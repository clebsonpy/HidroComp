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
    def get_spells(data_peaks, month_water):
        df_spells = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Complete', 'Name'])
        index = 0
        dates = pd.date_range(start=pd.to_datetime('1/%s/1998' % month_water[0], dayfirst=True), periods=365, freq='D')

        if len(data_peaks) > 0:
            inter = data_peaks['Peaks'].max() - data_peaks['Peaks'].min()
            for groups in data_peaks.groupby(pd.Grouper(freq=month_water[1])):
                for i in groups[1].index:

                    df_spells.at[index, 'Complete'] = 100-(100*(data_peaks['Peaks'].max() - data_peaks['Peaks'].loc[i])/inter)
                    start = data_peaks['Start'].loc[i]
                    end = data_peaks['End'].loc[i]
                    df_spells.at[index, 'Name'] = data_peaks['Peaks'].loc[i]
                    df_spells.at[index, 'Task'] = int(groups[0].year)
                    len_days = len(pd.date_range(start, end))
                    for date in dates:

                        if date.month == start.month and date.day == start.day:
                            inter_date = pd.date_range(start=date, periods=len_days)
                            if inter_date[-1] > dates[-1]:
                                date_start = pd.to_datetime(
                                    '%s/%s/%s' % (inter_date[0].day, inter_date[0].month, inter_date[0].year - 1),
                                    dayfirst=True)
                                date_end = pd.to_datetime(
                                    '%s/%s/%s' % (inter_date[-1].day, inter_date[-1].month, inter_date[-1].year - 1),
                                    dayfirst=True)

                                df_spells.at[index, 'Start'] = date_start
                                df_spells.at[index, 'Finish'] = date_end
                            else:

                                df_spells.at[index, 'Start'] = inter_date[0]
                                df_spells.at[index, 'Finish'] = inter_date[-1]
                    index += 1
                else:
                    pass

        return df_spells, index, dates[0], dates[-1]
