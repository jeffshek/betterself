from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.events.tests import User
from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from events.models import SupplementEvent
from supplements.models import Supplement


class SupplementAnalyticsSummaryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_user, _ = User.objects.get_or_create(username='default')
        builder = DemoHistoricalDataBuilder(cls.default_user)
        builder.create_historical_fixtures()

        supplement = Supplement.objects.filter(user=cls.default_user).first()
        supplement_uuid = str(supplement.uuid)
        cls.supplement = supplement
        cls.url = reverse('supplement-analytics-summary', args=[supplement_uuid])

        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(self.default_user)

    def test_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        expected_keys = {'productivity_correlation',
                         'sleep_correlation',
                         'most_taken',
                         'most_taken_dates',
                         'creation_date'}

        returned_keys = [list(items.keys())[0] for items in response.data]
        returned_keys = set(returned_keys)
        self.assertEqual(expected_keys, returned_keys)

        first_event = SupplementEvent.objects.filter(supplement=self.supplement).order_by('time').first()
        for data in response.data:
            # taking a step back and thinking about this, the whole dict within key structure is stupid
            if list(data.keys())[0] == 'creation_date':
                self.assertEqual(first_event.time.isoformat(), data['creation_date']['value'])
