from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder

# python manage.py test apis.betterself.v1.events.tests.test_sleep_views
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
        print (url)

    def test_sleep_averages_view(self):
        url = reverse('sleep-averages')
        print (url)

    def test_sleep_activities_correlations_view(self):
        url = reverse('sleep-activities-correlations')
        print (url)

    def test_sleep_supplements_view(self):
        url = reverse('sleep-supplements-correlations')
        print (url)
