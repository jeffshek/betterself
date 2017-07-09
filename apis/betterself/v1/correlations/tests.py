from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from constants import SLEEP_MINUTES_COLUMN
from events.models import SupplementEvent
from supplements.models import Supplement

User = get_user_model()


# python manage.py test apis.betterself.v1.correlations.tests

class BaseCorrelationsMixin(object):
    def test_view_with_user_and_no_data(self):
        user = User.objects.create(username='something-new')
        client = APIClient()
        client.force_authenticate(user)

        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data)


class BaseCorrelationsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = reverse(cls.url_namespace)
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='demo')

        builder = DemoHistoricalDataBuilder(cls.user)
        builder.create_historical_fixtures()

        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        super().setUp()


class ProductivitySupplementCorrelationsTests(BaseCorrelationsTests, BaseCorrelationsMixin):
    url_namespace = 'productivity-supplements-correlations'

    def test_productivity_supplements_correlation_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        # the correlation of the productivity driver (which will be the first result of the dataset) will be 1
        self.assertEqual(response.data[0][1], 1)

    def test_productivity_supplements_response_includes_correct_supplements(self):
        response = self.client.get(self.url)

        supplements_in_response = [item[0] for item in response.data]
        # don't include the productivity driver since that's not a supplement
        supplements_in_response = supplements_in_response[1:]

        user_supplements_ids = SupplementEvent.objects.filter(user=self.user).values_list('supplement_id', flat=True)
        user_supplements_ids = set(user_supplements_ids)
        # the user filter is just for safe keeping, shouldn't really be necessary
        user_supplements = Supplement.objects.filter(id__in=user_supplements_ids, user=self.user).values_list('name',
                                                                                                              flat=True)

        self.assertCountEqual(supplements_in_response, user_supplements)


class SleepSupplementsCorrelationsTests(BaseCorrelationsTests, BaseCorrelationsMixin):
    url_namespace = 'sleep-supplements-correlations'

    def test_sleep_supplements_view(self):
        response = self.client.get(self.url)

        self.assertTrue(SLEEP_MINUTES_COLUMN in response.data[0])
        # Return back in a tuple format to preserve order when transmitting as JSON
        self.assertEqual(response.data[0][0], SLEEP_MINUTES_COLUMN)
        self.assertEqual(response.data[0][1], 1)
        self.assertEqual(response.status_code, 200)


class SleepUserActivitiesCorrelationsTests(BaseCorrelationsTests, BaseCorrelationsMixin):
    url_namespace = 'sleep-user-activities-correlations'

    def test_sleep_activities_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        # the correlation of sleep to itself will be one
        self.assertEqual(response.data[0][1], 1)


class ProductivityUserActivitiesCorrelationsTests(BaseCorrelationsTests, BaseCorrelationsMixin):
    url_namespace = 'productivity-user-activities-correlations'

    def test_correlations_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        # the correlation of a variable to itself will be one
        self.assertEqual(response.data[0][1], 1)
