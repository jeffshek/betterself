from django.contrib.auth import get_user_model
from django.test import TestCase

from analytics.events.utils.dataframe_builders import SupplementEventsDataframeBuilder, SUPPLEMENT_EVENT_COLUMN_MAP, \
    TIME_COLUMN_NAME, ProductivityLogEventsDataframeBuilder, SleepActivityDataframeBuilder
from analytics.events.utils.aggregate_dataframe_builders import AggregateSupplementProductivityDataframeBuilder
from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from betterself.users.tests.mixins.test_mixins import UsersTestsFixturesMixin
from events.fixtures.mixins import SupplementEventsFixturesGenerator, ProductivityLogFixturesGenerator
from events.models import SupplementEvent, DailyProductivityLog, SleepActivity
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from vendors.fixtures.mixins import VendorModelsFixturesGenerator


User = get_user_model()


# python manage.py test analytics.events.tests.test_dataframe_builders
class TestSupplementEventDataframeBuilder(TestCase, UsersTestsFixturesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.create_user_fixtures()
        SupplementModelsFixturesGenerator.create_fixtures()
        VendorModelsFixturesGenerator.create_fixtures()
        SupplementEventsFixturesGenerator.create_fixtures(cls.user_1)

    def test_build_dataframe(self):
        queryset = SupplementEvent.objects.all()
        builder = SupplementEventsDataframeBuilder(queryset)

        # to prevent another brain fart moment, this is NOT the aggregated dataframe
        # this merely represents all the values as a rows of data before any pivot_table
        # or data transformations happen on it
        df = builder.build_dataframe()

        self.assertEqual(len(df.index), queryset.count())

    def test_build_dataframe_col_named_correctly(self):
        queryset = SupplementEvent.objects.all()
        builder = SupplementEventsDataframeBuilder(queryset)
        df = builder.build_dataframe()

        column_labels = list(SUPPLEMENT_EVENT_COLUMN_MAP.values())
        # time is an index location, so shouldn't be considered a column
        column_labels.remove(TIME_COLUMN_NAME)

        # really misleading, but this is the equivalent of what one would expect from "assertItemsEqual"
        self.assertCountEqual(column_labels, df.columns.tolist())

    def test_build_flat_dataframe(self):
        queryset = SupplementEvent.objects.all()
        builder = SupplementEventsDataframeBuilder(queryset)

        df = builder.get_flat_daily_dataframe()
        # get a list of all the "days" we have stored - ie. transform
        # a datetime to just a date. then compare that the builder's grouped daily
        times_values = SupplementEvent.objects.all().values_list('time', flat=True)

        unique_dates = {item.date() for item in times_values}
        df_dates = {item.date() for item in df.index}

        self.assertSetEqual(unique_dates, df_dates)


# python manage.py test analytics.events.tests.test_dataframe_builders.ProductivityLogEventsDataframeBuilderTests
class ProductivityLogEventsDataframeBuilderTests(TestCase, UsersTestsFixturesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.create_user_fixtures()
        ProductivityLogFixturesGenerator.create_fixtures(cls.user_1)
        super().setUpTestData()

    def test_build_dataframe(self):
        queryset = DailyProductivityLog.objects.all()
        builder = ProductivityLogEventsDataframeBuilder(queryset)

        df = builder.build_dataframe()
        valid_columns = ['Distracting Minutes', 'Neutral Minutes', 'Productive Minutes',
            'Source', 'Very Distracting Minutes', 'Very Productive Minutes']

        df_columns = df.keys().tolist()
        self.assertCountEqual(valid_columns, df_columns)

    def test_build_dataframe_has_no_missing_days(self):
        queryset = DailyProductivityLog.objects.all()
        builder = ProductivityLogEventsDataframeBuilder(queryset)

        queryset_count = queryset.count()

        df = builder.build_dataframe()
        self.assertEqual(df.index.size, queryset_count)

    def test_get_productive_timeseries(self):
        queryset = DailyProductivityLog.objects.all()
        builder = ProductivityLogEventsDataframeBuilder(queryset)
        df = builder.build_dataframe()

        first_event = df.iloc[0]
        # change to a dictionary for easier looping
        first_event_dict = first_event.to_dict()
        first_productive_time = sum(
            value for key, value in first_event_dict.items()
            if 'Productive' in key
        )

        productive_ts = builder.get_productive_timeseries()

        self.assertEqual(first_productive_time, productive_ts[0])

    def test_get_unproductive_timeseries(self):
        """
        Kind of a simple test, not the greatest - compare the first result and make sure it's valid
        """
        queryset = DailyProductivityLog.objects.all()
        builder = ProductivityLogEventsDataframeBuilder(queryset)

        df = builder.build_dataframe()
        first_event = df.iloc[0]

        # change to a dictionary for easier looping
        first_event_dict = first_event.to_dict()
        first_unproductive_time = sum(
            value for key, value in first_event_dict.items()
            if 'Productive' not in key
            and 'Minutes' in key
        )

        unproductive_ts = builder.get_unproductive_timeseries()

        self.assertEqual(first_unproductive_time, unproductive_ts[0])


# python manage.py test analytics.events.tests.test_dataframe_builders
class TestDataframeConcatenation(TestCase, UsersTestsFixturesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.create_user_fixtures()
        SupplementModelsFixturesGenerator.create_fixtures()
        VendorModelsFixturesGenerator.create_fixtures()
        SupplementEventsFixturesGenerator.create_fixtures(cls.user_1)
        ProductivityLogFixturesGenerator.create_fixtures(cls.user_1)

    def test_dataframe_composition(self):
        supplement_event_queryset = SupplementEvent.objects.all()
        productivity_log_queryset = DailyProductivityLog.objects.all()
        builder = AggregateSupplementProductivityDataframeBuilder(supplement_event_queryset=supplement_event_queryset,
                                                                  productivity_log_queryset=productivity_log_queryset)
        dataframe = builder.build_daily_dataframe()

        distinct_supplement_event_times = supplement_event_queryset.values_list('time', flat=True).distinct()
        distinct_supplement_event_dates = {item.date() for item in distinct_supplement_event_times}

        distinct_productivity_log_queryset_dates = productivity_log_queryset.values_list('date', flat=True).distinct()
        distinct_productivity_log_queryset_dates = {item for item in distinct_productivity_log_queryset_dates}

        distinct_dates = distinct_supplement_event_dates.union(distinct_productivity_log_queryset_dates)
        distinct_dates_count = len(distinct_dates)

        self.assertEqual(distinct_dates_count, dataframe.index.size)

    def test_dataframe_composition_with_no_data(self):
        # we always create fixtures per each test, so nothing really exists with 9000 fixtures
        supplement_event_queryset = SupplementEvent.objects.filter(id='9000')
        productivity_log_queryset = DailyProductivityLog.objects.filter(id='9000')

        builder = AggregateSupplementProductivityDataframeBuilder(supplement_event_queryset, productivity_log_queryset)
        dataframe = builder.build_daily_dataframe()

        self.assertTrue(dataframe.empty)


class SleepDataframeBuilderTests(TestCase, UsersTestsFixturesMixin):
    # shares some overlap with the tests in api/*, but those tests are probably doing a bit too much.
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='flying-duck')

        builder = DemoHistoricalDataBuilder(cls.user)
        builder.create_sleep_fixtures()

        super().setUpTestData()

    def test_sleep_dataframe_map_correct_date_to_sleep_time(self):
        sleep_queryset = SleepActivity.objects.filter(user=self.user)
        builder = SleepActivityDataframeBuilder(sleep_queryset)
        dataframe = builder.get_sleep_history_series()

        latest_sleep_record = sleep_queryset[0]
        latest_sleep_record_start_date = latest_sleep_record.start_time.date()
        latest_sleep_record_end_date = latest_sleep_record.end_time.date()

        # because the dataframe builder will represent sleep as a showcase of how much you slept that night ...
        # ie if you sleep on monday from 8pm to 8am, it will show monday as 12 hours, you would expect the dataframe
        # index to contain monday, but not tuesday's date (at least per the latest record)
        self.assertTrue(latest_sleep_record_start_date in dataframe.index)
        self.assertFalse(latest_sleep_record_end_date in dataframe.index)
