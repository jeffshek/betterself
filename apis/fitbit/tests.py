from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.fitbit.views import FitbitUserUpdateSleepHistory

User = get_user_model()


class FitbitSerializerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, _ = User.objects.get_or_create(username='default')
        self.client.force_authenticate(self.user)

        super().setUp()

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(FitbitUserUpdateSleepHistory.url)
        super().setUpTestData()

    def test_post_fails_for_empty_fitbit_update(self):

        # no post parameters should not work
        response = self.client.post(self.url)

        self.assertTrue('Missing' in response.data)
        self.assertEqual(response.status_code, 400)

    def test_post_fails_with_crappy_dates(self):
        data = {
            'start_date': 'jungle',
            'end_date': '2017-01-01'
        }
        response = self.client.post(self.url, data=data)
        # because start_date is messed up, it should complain about it
        self.assertTrue('start_date' in response.data)
        self.assertEqual(response.status_code, 400)

    def test_view_with_valid_parameters(self):
        """ Should just work. Famous Last Words"""
        data = {
            'start_date': '2016-1-1',
            'end_date': '2017-01-01'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 202)

    def test_view_with_invalid_parameters_of_start_date_greater_than_last(self):
        data = {
            'start_date': '2017-2-1',
            'end_date': '2017-01-01'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
