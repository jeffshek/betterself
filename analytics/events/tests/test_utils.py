from django.test import TestCase

from analytics.events.utils import SupplementEventsDataframeBuilder, SupplementEventColumnMapping, TIME_COLUMN_NAME, \
    ProductivityLogEventsDataframeBuilder
from betterself.users.tests.mixins.test_mixins import UsersTestsFixturesMixin
from events.fixtures.mixins import EventModelsFixturesGenerator, ProductivityLogFixturesGenerator
from events.models import SupplementEvent, DailyProductivityLog
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from vendors.fixtures.mixins import VendorModelsFixturesGenerator


# python manage.py test analytics.events.tests.test_utils
class TestSupplementEventDataframeBuilder(TestCase, UsersTestsFixturesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.create_user_fixtures()
        SupplementModelsFixturesGenerator.create_fixtures()
        VendorModelsFixturesGenerator.create_fixtures()
        EventModelsFixturesGenerator.create_fixtures(cls.user_1)

    def test_build_dataframe(self):
        queryset = SupplementEvent.objects.all()
        builder = SupplementEventsDataframeBuilder(queryset)
        df = builder.build_dataframe()

        self.assertEqual(len(df.index), queryset.count())

    def test_build_dataframe_col_named_correctly(self):
        queryset = SupplementEvent.objects.all()
        builder = SupplementEventsDataframeBuilder(queryset)
        df = builder.build_dataframe()

        column_labels = list(SupplementEventColumnMapping.values())
        # time is an index location, so shouldn't be considered a column
        column_labels.remove(TIME_COLUMN_NAME)

        # really misleading, but this is assertItemsEqual
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


# python manage.py test analytics.events.tests.test_utils.ProductivityLogEventsDataframeBuilderTests
class ProductivityLogEventsDataframeBuilderTests(TestCase, UsersTestsFixturesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.create_user_fixtures()
        ProductivityLogFixturesGenerator.create_fixtures(cls.user_1)
        super().setUpTestData()

    def setUp(self):
        super().setUp()

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
