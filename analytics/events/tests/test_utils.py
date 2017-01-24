from django.test import TestCase

from analytics.events.utils import SupplementEventsDataframeBuilder, SupplementEventColumnMapping, TIME_COLUMN_NAME, \
    QUANTITY_COLUMN_NAME
from betterself.users.tests.mixins.test_mixins import UsersTestsFixturesMixin
from events.fixtures.mixins import EventModelsFixturesGenerator
from events.models import SupplementEvent
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

    def test_build_daily_dataframe_sums(self):
        """
        Test that we can get DataFrames that are grouped correctly by day
        """
        queryset = SupplementEvent.objects.all()
        builder = SupplementEventsDataframeBuilder(queryset)

        df = builder.build_dataframe_grouped_daily()
        quantity_sum = df[QUANTITY_COLUMN_NAME].sum()

        quantities_values = SupplementEvent.objects.all().values_list('quantity', flat=True)
        quantities_values = sum(quantities_values)

        # if this is done correctly, the sum of the grouped by values
        # should be the same as the database
        self.assertEqual(quantity_sum, quantities_values)

    def test_build_flat_dataframe(self):
        queryset = SupplementEvent.objects.all()
        builder = SupplementEventsDataframeBuilder(queryset)

        df = builder.build_flat_dataframe()
        # get a list of all the "days" we have stored - ie. transform
        # a datetime to just a date. then compare that the builder's grouped daily
        times_values = SupplementEvent.objects.all().values_list('time', flat=True)

        unique_dates = {item.date() for item in times_values}
        df_dates = {item.date() for item in df.index}

        self.assertSetEqual(unique_dates, df_dates)
