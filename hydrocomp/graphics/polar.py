import plotly.graph_objs as go
import pandas as pd


class Polar(object):

    def __init__(self, df_events):
        self.df_events = df_events

    def year_polar(self):
        date_julian = list(map(int, pd.DatetimeIndex(self.df_events.index.values).strftime("%j")))
        date_julian_polar = [(i/366)*360 for i in date_julian]
        df_events_julian = self.df_events.copy()
        df_events_julian['DateJulian'] = date_julian
        df_events_julian['DateJulianPolar'] = date_julian_polar
        print(df_events_julian)
        return df_events_julian

    def plot(self, width=None, height=None, size_text=None, title=None):
        dicMes = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set",
                  "Out", "Nov", "Dez"]
        df_polar = self.year_polar()
        position = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]

        trace = go.Scatterpolar(
            r=df_polar.peaks.values,  # Vazao
            theta=df_polar.DateJulianPolar.values,  # Data
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
            name=title
        )

        data = [trace]
        angularX = go.layout.AngularAxis(
            showticklabels=False,
        )

        layout = dict(
            angularaxis=angularX,
            title=dict(text=title, x=0.5, xanchor='center', y=0.95, yanchor='top',
                       font=dict(family='Courier New, monospace', color='#7f7f7f', size=size_text + 6)),
            width=width, height=height,
            font=dict(family='Courier New, monospace', size=size_text, color='#7f7f7f'),
            showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                radialaxis=dict(showticklabels=True),
                angularaxis=dict(showticklabels=True, ticks='', tickvals=position, ticktext=dicMes)
            )
        )

        fig = dict(data=data, layout=layout)
        return fig, data
