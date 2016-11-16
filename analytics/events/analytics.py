from django.core.exceptions import ValidationError
from numpy import dtype

VALID_CORRELATION_METHODS = ['pearson', 'spearman', 'kendall']
ROLLABLE_COLUMN_TYPES = {dtype('float64'), dtype('int64')}


class DataFrameEventsAnalyzer(object):
    """
    Takes a DataFrame and returns analytics on top of it.
    """

    def __init__(self, dataframe, ignore_columns=None, rest_day_column=None):
        # certain columns might be just notes or useless information that can be ignored
        dataframe_cols = dataframe.columns
        # maybe ignore is a bad name ... non-weighted columns? something that implies
        # that it shouldn't be used in correlation analysis
        if ignore_columns:
            assert isinstance(ignore_columns, list)
            self.ignore_columns = ignore_columns
            self.valid_columns = [item for item in dataframe_cols if item not in ignore_columns]
        else:
            self.ignore_columns = []
            self.valid_columns = dataframe_cols

        # if it's a rest day, the correlations shouldn't be used. ie. if you're drinking caffeine on
        # Sunday and wasn't intending to get any work done, then those days shouldn't be used to measure how effective
        # caffeine is.
        if rest_day_column:
            assert isinstance(rest_day_column, str)
            dataframe = dataframe[dataframe[rest_day_column] == False]  # noqa

        self.dataframe = dataframe

    @classmethod
    def add_yesterday_shifted_to_dataframe(cls, dataframe):
        valid_columns = cls.get_rollable_columns(dataframe)

        dataframe = dataframe.copy()

        for col in valid_columns:
            # Advil - Yesterday
            shifted_col_name = '{0} - Yesterday'.format(col)
            series = dataframe[col]
            shifted_series = series.shift(1)
            dataframe[shifted_col_name] = shifted_series

        return dataframe

    def _get_cleaned_dataframe_copy(self, measurement, add_yesterday_lag, method):
        self._validate_correlation_method(method)
        # copy lets me be certain each result doesn't mess up state
        dataframe = self.dataframe.copy()

        if add_yesterday_lag:
            dataframe = self.add_yesterday_shifted_to_dataframe(dataframe)

        dataframe = self._remove_invalid_measurement_days(dataframe, measurement)
        return dataframe

    @staticmethod
    def _get_correlation_from_dataframe(dataframe, measurement, method, min_periods):
        correlation_results = dataframe.corr(method, min_periods)[measurement]
        correlation_results_sorted = correlation_results.sort_values(inplace=False)
        return correlation_results_sorted

    def get_correlation_for_measurement(self, measurement, add_yesterday_lag=False, method='pearson', min_periods=1):
        """
        :param measurement: Measurement is the column name of what you're trying to improve / correlate
        :param add_yesterday_lag: factor if you drank coffee yesterday
        :param method: see pandas documentation
        :param min_periods: see pandas documentation
        :return: correlation series
        """
        # i love you pandas, you make my life so easy
        dataframe = self._get_cleaned_dataframe_copy(measurement, add_yesterday_lag=add_yesterday_lag, method=method)
        correlation_results_sorted = self._get_correlation_from_dataframe(dataframe, measurement, method, min_periods)
        return correlation_results_sorted

    def get_correlation_across_summed_days_for_measurement(self, measurement, add_yesterday_lag=False, window=7,
            method='pearson', min_periods=1):
        dataframe = self._get_cleaned_dataframe_copy(measurement, add_yesterday_lag=add_yesterday_lag, method=method)

        rolled_dataframe = self.get_rolled_dataframe(dataframe, window)

        # update means any of the valid columns that could be updated ... are
        dataframe.update(rolled_dataframe)

        # don't care about entire rows that are NaN because they won't have a sum
        dataframe = dataframe.dropna(how='all')

        # for anything that isn't filled in, assume those are zeros, kind of have to because we're summing
        dataframe = dataframe.fillna(0)

        correlation_results_sorted = self._get_correlation_from_dataframe(dataframe, measurement, method, min_periods)
        return correlation_results_sorted

    @staticmethod
    def get_rollable_columns(dataframe):
        # not all dataframe columns are rollable ... the original source (excel) should already have them
        # listed as minutes, so don't try to sum up Time objects
        dataframe_col_types = dataframe.dtypes
        dataframe_rollable_columns = [col_name for col_name, col_type in dataframe_col_types.items() if col_type in
            ROLLABLE_COLUMN_TYPES]
        return dataframe_rollable_columns

    @classmethod
    def get_rolled_dataframe(cls, dataframe, window, min_periods=None):
        dataframe_rollable_columns = cls.get_rollable_columns(dataframe)

        rollable_dataframe = dataframe[dataframe_rollable_columns]
        # haven't figured out the right way to deal with min_periods
        # the thinking is that this rolling function should not be as forgiving
        # instead, maybe have the serializer replace NaN data with zeroes at that step
        # since "unfilled data" frequently just means None
        rolled_dataframe = rollable_dataframe.rolling(window=window, center=False).sum()

        return rolled_dataframe

    @staticmethod
    def _remove_invalid_measurement_days(dataframe, measurement):
        """
        if productivity is marked as zero, that shouldn't be used to measure effectiveness
        since it's almost impossible to get a zero using RescueTime as a productive driver
        this might not be the best measurement ... perhaps serializer should just fill with np.NaN
        so when you get the data here you can make a more accurate decision to scrap
        """
        valid_days = dataframe[measurement] != 0
        dataframe = dataframe[valid_days]
        return dataframe

    @staticmethod
    def _validate_correlation_method(method):
        if not isinstance(method, str):
            raise ValidationError('Correlation must be a string')

        if method not in VALID_CORRELATION_METHODS:
            raise ValidationError('Correlation must be one of {0} methods'.format(VALID_CORRELATION_METHODS))

    @classmethod
    def get_dataframe_event_count(cls, dataframe):
        rollable_columns = cls.get_rollable_columns(dataframe)
        event_count = {}
        for col in rollable_columns:
            series = dataframe[col]
            series_count = series[series != 0].count()
            event_count[col] = series_count
        return event_count
