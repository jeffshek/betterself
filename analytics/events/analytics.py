class DataFrameEventsAnalyzer(object):
    """
    Takes a DataFrame and returns analytics on top of it.
    """
    def __init__(self, dataframe, ignore_columns=None, rest_day_column_name=None):

        if ignore_columns:
            assert isinstance(ignore_columns, list)
            self.ignore_columns = ignore_columns
        else:
            self.ignore_columns = []

        # if it's a rest day, the correlations shouldn't be used. ie. if you're drinking caffeine on
        # Sunday and wasn't intending to get any work done, then those days shouldn't be used to measure how effective
        # caffeine is.
        if rest_day_column_name:
            assert isinstance(rest_day_column_name, str)
            dataframe = dataframe[dataframe[rest_day_column_name] == False]  # noqa

        dataframe_cols = dataframe.columns
        valid_columns = [item for item in dataframe_cols if item not in ignore_columns]

        self.valid_columns = valid_columns
        self.dataframe = dataframe

    @staticmethod
    def _add_yesterday_correlation_to_dataframe(dataframe, valid_columns):
        for col in valid_columns:
            # Advil - Yesterday
            shifted_col_name = '{0} - Yesterday'.format(col)
            series = dataframe[col]
            shifted_series = series.shift(1)
            dataframe[shifted_col_name] = shifted_series

        return dataframe

    def get_correlation_for_measurement(self, measurement, lookback_correlation=None):
        """ IE. What DataFrame effect are you trying to correlate this to? """
        if lookback_correlation:
            dataframe = self._add_yesterday_correlation_to_dataframe(self.dataframe)
        else:
            dataframe = self.dataframe.copy()

        # if productivity is marked as zero, that shouldn't be used to measure effectiveness
        # since it's almost impossible to get a zero using RescueTime as a productive driver
        # this might not be the best measurement ... perhaps serializer should just fill with np.NaN
        # so when you get the data here you can make a more accurate decision
        valid_days = dataframe[measurement] != 0
        dataframe = dataframe[valid_days]

        correlation_results = dataframe.corr()[measurement]
        correlation_results_sorted = correlation_results.sort_values(inplace=False)

        return correlation_results_sorted
