from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.constants import UNIQUE_KEY_CONSTANT
from apis.betterself.v1.events.tests import User
from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from events.models import SupplementEvent
from supplements.models import Supplement


class BaseSupplementAnalyticsTests(TestCase):
    @classmethod
    def setUpAnalyticsData(cls):
        cls.default_user, _ = User.objects.get_or_create(username='default')
        builder = DemoHistoricalDataBuilder(cls.default_user)
        builder.create_historical_fixtures()

        supplement = Supplement.objects.filter(user=cls.default_user).first()
        cls.supplement = supplement

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(self.default_user)


class SupplementAnalyticsSummaryTests(BaseSupplementAnalyticsTests):
    @classmethod
    def setUpTestData(cls):
        cls.setUpAnalyticsData()
        cls.url = reverse('supplement-analytics-summary', args=[str(cls.supplement.uuid)])

        super().setUpTestData()

    def test_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        expected_keys = {'productivity_correlation',
            'sleep_correlation',
            'most_taken',
            'most_taken_dates',
            'creation_date'}

        response_keys = set([item[UNIQUE_KEY_CONSTANT] for item in response.data])
        self.assertEqual(expected_keys, response_keys)

        first_event = SupplementEvent.objects.filter(supplement=self.supplement).order_by('time').first()
        for data in response.data:
            if data[UNIQUE_KEY_CONSTANT] == 'creation_date':
                self.assertEqual(first_event.time.isoformat(), data['value'])


class SupplementAnalyticsSleepTest(BaseSupplementAnalyticsTests):
    @classmethod
    def setUpTestData(cls):
        cls.setUpAnalyticsData()
        cls.url = reverse('supplement-analytics-sleep', args=[str(cls.supplement.uuid)])
        super().setUpTestData()

    def test_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class SupplementAnalyticsProductivityTest(BaseSupplementAnalyticsTests):
    @classmethod
    def setUpTestData(cls):
        cls.setUpAnalyticsData()
        cls.url = reverse('supplement-analytics-productivity', args=[str(cls.supplement.uuid)])
        super().setUpTestData()

    def test_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
