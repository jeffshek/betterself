from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.events.tests.views.test_views import User
from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from apis.betterself.v1.tests.mixins.test_post_requests import PostRequestsTestsMixin
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from events.models import SupplementReminder
from supplements.models import Supplement


class TestSupplementReminderViews(BaseAPIv1Tests, PostRequestsTestsMixin):
    TEST_MODEL = SupplementReminder
    PAGINATION = False

    @classmethod
    def setUpTestData(cls):
        cls.user_1, _ = User.objects.get_or_create(username='default')

        builder = DemoHistoricalDataBuilder(cls.user_1)
        builder.create_historical_fixtures()
        builder.create_supplement_reminders(limit=4)

        cls.url = reverse(SupplementReminder.RESOURCE_NAME)
        super().setUpTestData()

    def setUp(self):
        supplement = Supplement.objects.filter(user=self.user_1).first()
        supplement_uuid = str(supplement.uuid)

        self.DEFAULT_POST_PARAMS = {
            'reminder_time': '15:20',
            'quantity': 5,
            'supplement_uuid': supplement_uuid
        }

        self.client_1 = self.create_authenticated_user_on_client(APIClient(), self.user_1)
        self.client_2 = self.create_authenticated_user_on_client(APIClient(), self.user_2)

    def test_post_when_over_limit(self):
        # hardcoded value of 5 to prevent spam
        supplements = Supplement.objects.filter(user=self.user_1)
        for supplement in supplements:
            params = {
                'reminder_time': '10:20',
                'quantity': 5,
                'supplement_uuid': str(supplement.uuid)
            }
            self.client_1.post(self.url, data=params)

        cutoff_limit = 5
        user_supplement_reminders = SupplementReminder.objects.filter(user=self.user_1).count()
        self.assertEqual(cutoff_limit, user_supplement_reminders)

    def test_view_no_auth(self):
        client = APIClient()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_view_no_data(self):
        new_user, _ = User.objects.get_or_create(username='no-data')

        client = APIClient()
        client.force_login(new_user)

        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_view(self):
        response = self.client_1.get(self.url)
        self.assertEqual(response.status_code, 200)

        supplement_reminder_count = SupplementReminder.objects.filter(user=self.user_1).count()
        self.assertEqual(supplement_reminder_count, len(response.data))
