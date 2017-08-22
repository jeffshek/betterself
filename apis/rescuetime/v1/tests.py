from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


class TestRescueTimeAPIPostView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = reverse('rescuetime-user-update-productivity-history')
        super().setUpClass()

    def setUp(self):
        user = User.objects.create_user(username='jacob', email='jacob@donkey.com', password='top_secret')
        self.user = user

        self.client = APIClient()
        self.client.force_login(self.user)
        super().setUp()

    def test_view_with_no_details_should_error(self):
        response = self.client.post(self.url)

        # should say Missing some key, etc. etc
        self.assertTrue('Missing' in response.data)
        self.assertEqual(response.status_code, 400)

    def test_view_with_incorrect_details_types_should_error(self):
        """ IE. pass a non-date to a date field """
        data = {
            'rescuetime_api_key': 'cat',
            'start_date': 'jungle',
            'end_date': '2017-01-01'
        }
        response = self.client.post(self.url, data=data)
        self.assertTrue('start_date' in response.data)
        self.assertEqual(response.status_code, 400)

    def test_view_with_valid_parameters(self):
        """ Should just work. """
        data = {
            'rescuetime_api_key': 'cat',
            'start_date': '2016-1-1',
            'end_date': '2017-01-01'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 202)

    def test_view_with_invalid_start_and_end_date_greater(self):
        data = {
            'rescuetime_api_key': 'cat',
            'start_date': '2017-2-1',
            'end_date': '2017-01-01'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
