import pandas as pd

from hidrocomp.eflow.exceptions import *
from hidrocomp.eflow.graphics import Graphics, GraphicsRVA


class RVA:

    def __init__(self, variable_pre, variable_pos, statistic, boundaries):
        self.data_pre = variable_pre
        self.data_pos = variable_pos
        self.boundaries = boundaries
        self.statistic = statistic
        self.name_variable = variable_pre.name
        self.line = self.__line()
        self.frequency_pre = self.__frequency(data_variable=self.data_pre.data)
        self.frequency_pos = self.__frequency(data_variable=self.data_pos.data)

    def measure_hydrologic_alteration(self):
        def very(rva):
            for i in rva:
                for j in rva[i].index:
                    if rva[i][j] < -1:
                        rva.iat[i, j] = -1
            return rva
        try:
            mha = (self.frequency_pos - self.frequency_pre) / self.frequency_pre
        except ZeroDivisionError:
            mha = (self.frequency_pos - self.frequency_pre)
        return very(mha)

    def __line(self):

        print(self.name_variable)

        line = pd.DataFrame(columns=['lower_line', 'upper_line', 'median_line'])

        if self.statistic == 'non-parametric':
            line.at[self.name_variable, 'lower_line'] = self.data_pre.data.quantile((50 - self.boundaries) / 100)
            line.at[self.name_variable, 'upper_line'] = self.data_pre.data.quantile((50 + self.boundaries) / 100)
            line.at[self.name_variable, 'median_line'] = self.data_pre.data.median()
            return line
        elif self.statistic == 'parametric':
            line.at[self.name_variable,
                    'lower_line'] = self.data_pre.data[self.name_variable].mean() - self.data_pre.data[self.name_variable].std()
            line.at[self.name_variable,
                    'lower_line'] = self.data_pre.data[self.name_variable].mean() + self.data_pre.data[self.name_variable].std()
            line.at[self.name_variable, 'lower_line'] = self.data_pre.data[self.name_variable].median()
            return line
        else:
            raise NotStatistic('Not exist statistic {}: use {} or {}'.format(self.statistic,
                                                                             'non-parametric', 'parametric'), line=91)

    def __frequency(self, data_variable):
        count = pd.DataFrame(columns=['Lower', 'Median', 'Upper'])
        upper_line, lower_line = self.line['upper_line'], self.line['lower_line']
        if upper_line[self.name_variable] == 0 and lower_line[self.name_variable] == 0:
            count.at[self.name_variable, 'Lower'] = 0
            count.at[self.name_variable, 'Upper'] = 0
            count.at[self.name_variable, 'Median'] = 0
        else:
            boolean_lower = pd.DataFrame(data_variable.isin(
                data_variable.loc[data_variable <= lower_line[self.name_variable]]))
            boolean_upper = pd.DataFrame(data_variable.isin(
                data_variable.loc[data_variable >= upper_line[self.name_variable]]))
            boolean_median = pd.DataFrame(data_variable.isin(
                data_variable.loc[boolean_lower[self.name_variable] == boolean_upper[self.name_variable]]))

            count.at[self.name_variable, 'Lower'] = boolean_lower[
                self.name_variable].loc[boolean_lower[self.name_variable] == True].count()
            count.at[self.name_variable, 'Upper'] = boolean_upper[
                self.name_variable].loc[boolean_upper[self.name_variable] == True].count()
            count.at[self.name_variable, 'Median'] = boolean_median[
                self.name_variable].loc[boolean_median[self.name_variable] == True].count()
        return count

    def plot(self, color={"pre": "blue", "pos": "red"}):
        """
        @type color: dict
        """
        fig_obs, data_obs = GraphicsRVA(data_variable=self.data_pos, status="pos", color=color, line=self.line).plot()
        fig_nat, data_nat = GraphicsRVA(data_variable=self.data_pre, status="pre", color=color, line=self.line).plot()

        data = data_obs + [data_nat[0]]
        fig = dict(data=data, layout=fig_nat['layout'])

        return fig, data
