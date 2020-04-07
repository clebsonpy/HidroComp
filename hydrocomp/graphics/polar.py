import plotly as py
import plotly.graph_objs as go
import pandas as pd
import calendar
import datetime


class Polar(object):

    def __init__(self, df_events):
        self.df_events = df_events

    @staticmethod
    def julin(ano, day_julian):
        diasMes = calendar.monthrange(ano, 2)[1]
        if diasMes == 29:
            data = datetime.datetime.strptime('2000%s' % day_julian, '%Y%j')
        elif diasMes == 28:
            if day_julian > 59:
                data = datetime.datetime.strptime('2000%s' % (day_julian + 1), '%Y%j')
            else:
                data = datetime.datetime.strptime('2000%s' % day_julian, '%Y%j')
        return data

    def year_polar(self):
        date_julian = list(map(int, pd.DatetimeIndex(self.df_events.index.values).strftime("%j")))
        print(date_julian)
        date_jul_float = [(i/366)*360 for i in date_julian]
        self.df_events['DateJ'] = date_jul_float
        print(self.df_events)
        return self.df_events

    def plot(self):
        dicMes = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set",
                  "Out", "Nov", "Dez"]
        df_polar = self.year_polar()
        position = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]

        trace = go.Scatterpolar(
            r=df_polar.peaks.values,  # Vazao
            theta=df_polar.DateJ.values,  # Data
            mode='markers',
            marker=dict(
                color='rgb(27,158,119)',
                size=10,
                line=dict(
                    color='white'
                ),
                opacity=0.7),
            text=df_polar.index.date,
            thetaunit='degrees',
        )

        data = [trace]
        angularX = go.layout.AngularAxis(
            showticklabels=False,
        )

        layout = dict(
            angularaxis=angularX,
            title='',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            showlegend=False,
            polar=dict(
                radialaxis=dict(showticklabels=True),
                angularaxis=dict(showticklabels=True, ticks='', tickvals=position, ticktext=dicMes)
            )
        )

        fig = dict(data=data, layout=layout)
        return fig, data
