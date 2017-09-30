from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from betterself.users.models import UserPhoneNumber

User = get_user_model()


class TestUserPhoneNumber(TestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'testpassword')
        self.url = reverse('api-user-phone-number')

    def test_getting_of_phone_number(self):
        client = APIClient()
        client.force_login(self.test_user)

        UserPhoneNumber.objects.create(user=self.test_user, phone_number='+16175555555')

        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_access_of_phone_number_not_auth(self):
        client = APIClient()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_of_phone_number_no_data(self):
        client = APIClient()
        client.force_login(self.test_user)

        response = client.get(self.url)
        self.assertEqual(response.status_code, 204)

    def test_phone_number_update(self):
        client = APIClient()
        client.force_login(self.test_user)

        details = {
            'phone_number': '+16175555555'
        }

        response = client.post(self.url, data=details)
        self.assertEqual(response.status_code, 200)

    def test_phone_number_nonsense_update(self):
        client = APIClient()
        client.force_login(self.test_user)

        details = {
            'phone_number': 'abcde'
        }

        response = client.post(self.url, data=details)
        self.assertEqual(response.status_code, 400)
