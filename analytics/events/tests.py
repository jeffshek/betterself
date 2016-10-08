import datetime
import pandas as pd

from django.test import TestCase

# python manage.py test analytics.events.tests
from analytics.events.analytics import DataFrameEventsAnalyzer


class DataFrameEventsAnalyzerTests(TestCase):
    PRODUCTIVITY_COLUMN = 'Productivity'
    NEGATIVE_PRODUCTIVITY_COLUMN = 'Negativity'

    @classmethod
    def setUpTestData(cls):
        super(DataFrameEventsAnalyzerTests, cls).setUpTestData()

    def setUp(self):
        pass

    @staticmethod
    def _create_dataframe_fixture():
        # multiply by X because i'm too lazy to write random numbers
        multipler = 5
        caffeine_values = [100, 150, 200, 300, 300, 0, 150] * multipler
        theanine_values = [0, 150, 300, 150, 150, 0, 150] * multipler
        productivity_values = [.5, .9, .3, .6, .7, .2, .9] * multipler

        caffeine_series = pd.Series(caffeine_values)
        theanine_series = pd.Series(theanine_values)
        productivity_series = pd.Series(productivity_values)
        negative_correlation_series = productivity_series * -1

        # check no stupidity with mismatching periods
        assert len(caffeine_series) == len(theanine_series)
        assert len(caffeine_series) == len(productivity_series)

        dataframe = pd.DataFrame({
            'Caffeine': caffeine_series,
            'Theanine': theanine_series,
            DataFrameEventsAnalyzerTests.PRODUCTIVITY_COLUMN: productivity_series,
            DataFrameEventsAnalyzerTests.NEGATIVE_PRODUCTIVITY_COLUMN: negative_correlation_series,
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

    def test_rolling_correlation_analytics(self):
        dataframe = self._create_dataframe_fixture()
        analyzer = DataFrameEventsAnalyzer(dataframe)
        correlation = analyzer.get_correlation_across_summed_days_for_measurement(self.PRODUCTIVITY_COLUMN)

        self.assertTrue(correlation[self.PRODUCTIVITY_COLUMN] == 1)
        self.assertTrue(correlation[self.NEGATIVE_PRODUCTIVITY_COLUMN] == -1)
