import datetime
import pandas as pd

from django.test import TestCase

# python manage.py test analytics.events.tests
from analytics.events.analytics import DataFrameEventsAnalyzer


class DataFrameEventsAnalyzerTests(TestCase):
    PRODUCTIVITY_COLUMN = 'Productivity'
    NEGATIVE_PRODUCTIVITY_COLUMN = 'Negativity'
    SOME_POSITIVELY_CORRELATED_COLUMN = 'Happiness'

    @classmethod
    def setUpTestData(cls):
        super(DataFrameEventsAnalyzerTests, cls).setUpTestData()

    @staticmethod
    def _create_dataframe_fixture():
        # multiply by X because i'm too lazy to write random numbers
        multiplier = 5
        caffeine_values = [100, 150, 200, 300, 300, 0, 150] * multiplier
        # a bit of a random hack, but some absurd values just to make sure correlation is tested
        theanine_values = [0, 95000, 1300, 15, 4, -90000, 150] * multiplier
        productivity_values = [50, 90, 30, 60, 70, 20, 90] * multiplier

        caffeine_series = pd.Series(caffeine_values)
        theanine_series = pd.Series(theanine_values)
        productivity_series = pd.Series(productivity_values)
        negative_correlation_series = productivity_series * -1
        some_positively_correlated_series = productivity_series ** 1.3

        # check no stupidity with mismatching periods
        assert len(caffeine_series) == len(theanine_series)
        assert len(caffeine_series) == len(productivity_series)

        dataframe = pd.DataFrame({
            'Caffeine': caffeine_series,
            'Theanine': theanine_series,
            DataFrameEventsAnalyzerTests.PRODUCTIVITY_COLUMN: productivity_series,
            DataFrameEventsAnalyzerTests.NEGATIVE_PRODUCTIVITY_COLUMN: negative_correlation_series,
            DataFrameEventsAnalyzerTests.SOME_POSITIVELY_CORRELATED_COLUMN: some_positively_correlated_series,
        })

        # create date index to make dataframe act more like real data
        start_time = datetime.datetime(2016, 1, 1)
        dataframe_date_index = [start_time + datetime.timedelta(days=day) for day in range(0, len(caffeine_series))]

        dataframe.index = dataframe_date_index
        return dataframe

    def test_setting_of_analytics_dataframe(self):
        dataframe = self._create_dataframe_fixture()
        analyzer = DataFrameEventsAnalyzer(dataframe)

        self.assertIsInstance(analyzer.dataframe, pd.DataFrame)
        self.assertEqual(len(dataframe), len(analyzer.dataframe))

    def test_analytics_dataframe_with_invalid_correlation(self):
        dataframe = self._create_dataframe_fixture()
        analyzer = DataFrameEventsAnalyzer(dataframe)
        with self.assertRaises(KeyError):
            analyzer.get_correlation_for_measurement('non_existent_column')

    def test_correlation_analytics(self):
        dataframe = self._create_dataframe_fixture()
        analyzer = DataFrameEventsAnalyzer(dataframe)
        correlation = analyzer.get_correlation_for_measurement(self.PRODUCTIVITY_COLUMN)

        # about the only thing we could be certain of is productivity's correlation with itself should be 1
        self.assertTrue(correlation[self.PRODUCTIVITY_COLUMN] == 1)

    def test_correlation_analytics_includes_yesterday(self):
        dataframe = self._create_dataframe_fixture()
        analyzer = DataFrameEventsAnalyzer(dataframe)
        correlation = analyzer.get_correlation_for_measurement(self.PRODUCTIVITY_COLUMN, add_yesterday_lag=True)

        # about the only thing we could be certain of is productivity's correlation with itself should be 1
        correlation_includes_previous_day = any('Yesterday' in item for item in correlation.index)
        self.assertTrue(correlation_includes_previous_day)

    def test_rolling_correlation_analytics(self):
        dataframe = self._create_dataframe_fixture()
        analyzer = DataFrameEventsAnalyzer(dataframe)
        correlation = analyzer.get_correlation_across_summed_days_for_measurement(self.PRODUCTIVITY_COLUMN)

        self.assertTrue(correlation[self.PRODUCTIVITY_COLUMN] == 1)
        self.assertTrue(correlation[self.NEGATIVE_PRODUCTIVITY_COLUMN] == -1)
        # doing a lame non-linear transform to diverge from 1, but should generally indicate a positive correlation ...
        self.assertTrue(correlation[self.SOME_POSITIVELY_CORRELATED_COLUMN] > .9)

    def test_rolling_analytics_rolls(self):
        window = 7
        dataframe = self._create_dataframe_fixture()
        analyzer = DataFrameEventsAnalyzer(dataframe)
        rolled_dataframe = analyzer.get_rolled_dataframe(dataframe, window=window)
        last_rolled_results = rolled_dataframe.ix[-1]

        dataframe_columns = dataframe.keys()
        for column in dataframe_columns:
            # get the last window (ie. last 7 day results of the series)
            series = dataframe[column][-1 * window:].values
            series_sum = sum(series)

            last_rolled_results_column = last_rolled_results[column]

            self.assertEqual(series_sum, last_rolled_results_column)
