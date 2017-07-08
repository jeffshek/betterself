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
    def setUpTestData(cls):
        cls.user = User.objects.create(username='demo')

        builder = DemoHistoricalDataBuilder(cls.user)
        builder.create_sleep_fixtures()

        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_sleep_averages_view(self):
        url = reverse('sleep-averages')
        kwargs = {'lookback': 7}
        response = self.client.get(url, data=kwargs)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 1)

    def test_sleep_averages_returns_400_with_invalid_lookback(self):
        url = reverse('sleep-averages')
        kwargs = {'lookback': 'cat'}
        response = self.client.get(url, data=kwargs)
        self.assertEqual(response.status_code, 400)

    def test_sleep_averages_view_returns_400(self):
        url = reverse('sleep-averages')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)

    def test_sleep_averages_with_user_and_no_data(self):
        url = reverse('sleep-averages')
        user = User.objects.create(username='jack-in-box')
        client = APIClient()
        client.force_authenticate(user)

        kwargs = {'lookback': 7}

        response = client.get(url, data=kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {})
