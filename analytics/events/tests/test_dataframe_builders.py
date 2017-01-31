from django.test import TestCase

from analytics.events.utils.dataframe_builders import SupplementEventsDataframeBuilder, SUPPLEMENT_EVENT_COLUMN_MAP, \
    TIME_COLUMN_NAME, ProductivityLogEventsDataframeBuilder, AggregateDataframeBuilder
from betterself.users.tests.mixins.test_mixins import UsersTestsFixturesMixin
from events.fixtures.mixins import SupplementEventsFixturesGenerator, ProductivityLogFixturesGenerator
from events.models import SupplementEvent, DailyProductivityLog
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from vendors.fixtures.mixins import VendorModelsFixturesGenerator


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

        df = builder.get_flat_dataframe()
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
        builder = AggregateDataframeBuilder(supplement_event_queryset, productivity_log_queryset)
        dataframe = builder.build_dataframe()

        distinct_supplement_event_times = supplement_event_queryset.values_list('time', flat=True).distinct()
        distinct_supplement_event_dates = {item.date() for item in distinct_supplement_event_times}

        distinct_productivity_log_queryset_dates = productivity_log_queryset.values_list('date', flat=True).distinct()
        distinct_productivity_log_queryset_dates = {item for item in distinct_productivity_log_queryset_dates}

        distinct_dates = distinct_supplement_event_dates.union(distinct_productivity_log_queryset_dates)
        distinct_dates_count = len(distinct_dates)

        self.assertEqual(distinct_dates_count, dataframe.index.size)
