from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from events.models import SupplementEvent
from supplements.models import Supplement

User = get_user_model()


# python manage.py test apis.betterself.v1.correlations.tests


class ProductivitySupplementCorrelationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='demo')

        builder = DemoHistoricalDataBuilder(cls.user)
        builder.create_historical_fixtures()

        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_productivity_supplements_correlation_view(self):
        url = reverse('productivity-supplements-correlations')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # the correlation of the productivity driver (which will be the first result of the dataset)
        # will be 1
        self.assertEqual(response.data[0][1], 1)

    def test_productivity_supplements_response_includes_correct_supplements(self):
        url = reverse('productivity-supplements-correlations')
        response = self.client.get(url)

        supplements_in_response = [item[0] for item in response.data]
        # don't include the productivity driver since that's not a supplement
        supplements_in_response = supplements_in_response[1:]

        user_supplements_ids = SupplementEvent.objects.filter(user=self.user).values_list('supplement_id', flat=True)
        user_supplements_ids = set(user_supplements_ids)
        # the user filter is just for safe keeping, shouldn't really be necessary
        user_supplements = Supplement.objects.filter(id__in=user_supplements_ids, user=self.user).values_list('name',
                                                                                                              flat=True)

        self.assertCountEqual(supplements_in_response, user_supplements)

    def test_productivity_supplements_correlation_with_empty_user(self):
        url = reverse('productivity-supplements-correlations')

        user = User.objects.create(username='something-new')
        client = APIClient()
        client.force_authenticate(user)

        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data)
