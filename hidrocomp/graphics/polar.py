import plotly.graph_objs as go
import pandas as pd
import colorlover as cl


class Polar(object):

    def __init__(self, df_events):
        self.df_events = df_events

    def year_polar(self):
        date_julian = list(map(int, pd.DatetimeIndex(self.df_events.index.values).strftime("%j")))
        date_julian_polar = [(i/366)*360 for i in date_julian]
        df_events_julian = self.df_events.copy()
        df_events_julian['DateJulian'] = date_julian
        df_events_julian['DateJulianPolar'] = date_julian_polar
        return df_events_julian

    def color_bar(self, df_polar, color_bar_range: list):

        ylrd = cl.scales['9']['div']['Spectral'][::-1]

        if color_bar_range:
            year_color_bar = list(map(int, range(color_bar_range[0], color_bar_range[1]+1)))
        else:
            year_color_bar = df_polar.index.year.drop_duplicates()

        number_of_lines = len(year_color_bar)
        ylrd = cl.interp(ylrd, number_of_lines)
        colors = dict(zip(year_color_bar, ylrd))

        try:
            list_color = [colors[i] for i in df_polar.index.year]
        except KeyError:
            raise KeyError('O intervalo do dataframe ficou fora do intervalo do colorbar')

        colorbar_trace = go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(
                colorscale=ylrd,
                showscale=True,
                colorbar=dict(title='Anos'),
                cmin=year_color_bar[0],
                cmax=year_color_bar[-1],
            ),
        )

        return list_color, colorbar_trace

    def plot(self, width: int = None, height: int = None, size_text: int = None, title=None, color=None, name=None,
             showlegend: bool = False, language: str = 'pt', color_bar_range: list = None):
        list_month_pt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        list_month_en = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        dic_month = {'pt': list_month_pt, 'en': list_month_en}

        df_polar = self.year_polar()

        if color == 'by_year':
            list_color, colorbar_trace = self.color_bar(df_polar, color_bar_range)
            data = [colorbar_trace]

        else:
            list_color = color
            data = []

        position = [0, 31*0.9863, 59*0.9863, 90*0.9863, 120*0.9863, 151*0.9863, 181*0.9863, 212*0.9863, 243*0.9863,
                    273*0.9863, 303*0.9863, 334*0.9863]
        if len(df_polar) > 0:
            try:
                trace = go.Scatterpolar(
                    r=df_polar.Peaks.values,  # Vazao
                    theta=df_polar.DateJulianPolar.values,  # Data
                    mode='markers',
                    marker=dict(
                        color=list_color,
                        size=[10]*len(df_polar.Duration.values),
                        line=dict(
                            color='white'
                        ),
                        opacity=0.7),
                    text=['<b>Data</b>: {}<br>'
                          '<b>Duração</b>: {} dias'.format(i, j)
                          for i, j in zip(df_polar.index.date, df_polar.Duration.values)
                          ],
                    thetaunit='degrees',
                    name=name,
                    hovertemplate=
                    '<b>Dia Juliano</b>: %{theta:.2f}°<br>' +
                    '<b>Vazão</b>: %{r}<br>' +
                    '%{text}',
                )
            except AttributeError:
                trace = go.Scatterpolar(
                    r=df_polar.Peaks.values,  # Vazao
                    theta=df_polar.DateJulianPolar.values,  # Data
                    mode='markers',
                    marker=dict(
                        color=list_color,
                        size=10,
                        line=dict(
                            color='white'
                        ),
                        opacity=0.7),
                    thetaunit='degrees',
                    name=name
                )

        else:
            trace = go.Scatterpolar(
                r=None,  # Vazao
                theta=None,  # Data
                mode='markers',
                marker=dict(
                    color=list_color,
                    size=10,
                    line=dict(
                        color='white'
                    ),
                    opacity=0.7),
                thetaunit='degrees',
                name=name
            )

        data = data + [trace]

        xaxis = go.layout.XAxis(
            showticklabels=False,
            showgrid=False,
            showline=False,
        )
        yaxis = go.layout.YAxis(
            showticklabels=False,
            showgrid=False,
            showline=False,
        )

        layout = dict(
            title=dict(text=title, x=0.5, xanchor='center', y=0.95, yanchor='top',
                       font=dict(family='Courier New, monospace', color='rgb(0,0,0)', size=size_text + 6)),
            width=width+width*0.05, height=height,
            font=dict(family='Courier New, monospace', size=size_text, color='rgb(0,0,0)'),
            showlegend=showlegend, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
            polar=dict(
                radialaxis=dict(showticklabels=True, gridcolor="#000000"),
                angularaxis=dict(showticklabels=True, ticks='', tickvals=position, ticktext=dic_month[language],
                                 rotation=90, direction="clockwise", gridcolor="#000000", tickcolor="#000000"),
                bgcolor='#FFFFFF',
            ),
            xaxis=xaxis,
            yaxis=yaxis,
        )

        fig = dict(data=data, layout=layout)
        return fig, data
