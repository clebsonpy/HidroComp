import pandas as pd

class Partial(object):

    def __init__(self, data, threshold, station):
        self.data = data
        self.threshold = threshold
        self.station = station

    def peaks(self):
        events_threshold = self.__events_over_threshold(self.threshold)

        return events_threshold

    def __events_over_threshold(self, threshold=None):

        data = self.data.loc[self.data[self.station] > threshold, self.station].to_frame()
        date_start, date_end = self.__start_and_end(data=data)
        _data = pd.DataFrame(index=pd.date_range(start=date_start, end=date_end))

        data = _data.combine_first(data[date_start:date_end])
        print(data)

        return self.less_period(data=data)

    def __start_and_end(self, data):
        try:
            boolean = data.dropna(axis=0, how='all')
        except AttributeError:
            boolean = data
        date = boolean.index
        return date[0], date[-1]

    def less_period(self, data):
        """
        """
        aux = list()
        list_start = list()
        list_end = list()
        gantt_bool = data[self.station].isnull()
        print(gantt_bool)
        for i in gantt_bool.index:
            if ~gantt_bool.loc[i]:
                aux.append(i)
            elif len(aux) >= 1 and gantt_bool.loc[i]:
                list_start.append(aux[0])
                list_end.append(aux[-1])
                aux = []
        if len(aux) > 0:
            list_start.append(aux[0])
            list_end.append(aux[-1])

        dic = {'Start': list_start, 'Finish': list_end}
        return pd.DataFrame(dic)
