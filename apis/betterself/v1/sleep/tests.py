import math

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from events.models import SleepActivity

User = get_user_model()


class SleepAggregateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='demo')

        builder = DemoHistoricalDataBuilder(cls.user)
        builder.create_sleep_fixtures()

        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_sleep_aggregates_view(self):
        url = reverse('sleep-aggregates')
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)

        data = response.data
        first_date = min(data.keys())
        first_record_sleep_time = data[first_date]

        # check that the data from the view somewhat equals what the sleep duration should be
        # this test isn't fully exact, but didn't want to rebuild a time hashing algorithm for a test
        first_sleep_activity_record = SleepActivity.objects.filter(user=self.user).order_by('start_time').first()
        second_sleep_activity_record = SleepActivity.objects.filter(user=self.user).order_by('start_time')[1]

        # duration range
        min_duration_minutes = first_sleep_activity_record.duration.seconds / 60
        max_duration_minutes = math.ceil(min_duration_minutes + second_sleep_activity_record.duration.seconds / 60)

        first_record_falls_within_range = min_duration_minutes <= first_record_sleep_time < max_duration_minutes
        self.assertTrue(first_record_falls_within_range)

    def test_sleep_aggregates_with_user_and_no_data(self):
        url = reverse('sleep-aggregates')
        user = User.objects.create(username='jack-in-box-2')
        client = APIClient()
        client.force_authenticate(user)

        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {})


class SleepAverageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = reverse('sleep-averages')
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='demo')

        builder = DemoHistoricalDataBuilder(cls.user)
        builder.create_sleep_fixtures()

        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_sleep_averages_view(self):
        kwargs = {'lookback': 7}
        response = self.client.get(self.url, data=kwargs)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 1)

    def test_sleep_averages_returns_400_with_invalid_lookback(self):
        kwargs = {'lookback': 'cat'}
        response = self.client.get(self.url, data=kwargs)
        self.assertEqual(response.status_code, 400)

    def test_sleep_averages_view_returns_200(self):
        # if no params passed, should default to 1
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_sleep_averages_view_same_result_as_default_parameter(self):
        # for responses with the default params, it should equal
        # the same as something that didn't pass a lookback param
        default_response = self.client.get(self.url)

        kwargs = {'lookback': 1}
        second_response = self.client.get(self.url, data=kwargs)

        self.assertEqual(default_response.data, second_response.data)

    def test_sleep_averages_view_not_same_result_as_default_parameter(self):
        # for responses with different params, it should not equal equal default
        default_response = self.client.get(self.url)

        # default window is 1, so if this is 2, it should be different
        kwargs = {'lookback': 2}
        second_response = self.client.get(self.url, data=kwargs)

        self.assertNotEqual(default_response.data, second_response.data)

    def test_sleep_averages_with_user_and_no_data(self):
        user = User.objects.create(username='jack-in-box')
        client = APIClient()
        client.force_authenticate(user)

        kwargs = {'lookback': 7}

        response = client.get(self.url, data=kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {})
