import math
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder

# python manage.py test apis.betterself.v1.events.tests.test_sleep_views
from events.models import SleepActivity

User = get_user_model()


class ActivityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='demo')

        # kinda wish you had done this via a factory like everything else
        builder = DemoHistoricalDataBuilder(cls.user)
        builder.create_historical_fixtures()

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

    def test_sleep_averages_view(self):
        url = reverse('sleep-averages')
        self.assertTrue(url)

    def test_sleep_activities_correlations_view(self):
        url = reverse('sleep-activities-correlations')
        self.assertTrue(url)

    def test_sleep_supplements_view(self):
        url = reverse('sleep-supplements-correlations')
        self.assertTrue(url)
