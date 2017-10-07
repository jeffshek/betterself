from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from betterself.users.models import UserPhoneNumberDetails

User = get_user_model()


class TestUserPhoneNumber(TestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'testpassword')
        self.url = reverse('api-user-phone-number')

    def test_getting_of_phone_number(self):
        phone_number = '+16175555555'
        client = APIClient()
        client.force_login(self.test_user)

        UserPhoneNumberDetails.objects.create(user=self.test_user, phone_number=phone_number)

        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], phone_number)

    def test_access_of_phone_number_not_auth(self):
        client = APIClient()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_of_phone_number_no_data(self):
        client = APIClient()
        client.force_login(self.test_user)

        response = client.get(self.url)
        self.assertEqual(response.status_code, 204)

    def test_take_someone_else_number(self):
        original_number = '+6171234567'
        UserPhoneNumberDetails.objects.create(
            user=self.test_user, phone_number=original_number, is_verified=True)

        new_user = User.objects.create_user('new-user', 'testpassword')
        client = APIClient()
        client.force_login(new_user)
        details = {
            'phone_number': original_number
        }
        response = client.post(self.url, data=details)
        self.assertEqual(response.status_code, 400)

    def test_take_someone_else_number_not_verified(self):
        original_number = '+6171234567'
        UserPhoneNumberDetails.objects.create(user=self.test_user, phone_number=original_number)

        new_user = User.objects.create_user('new-user', 'testpassword')
        client = APIClient()
        client.force_login(new_user)
        details = {
            'phone_number': original_number
        }
        response = client.post(self.url, data=details)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], original_number)

    def test_phone_number_update(self):
        client = APIClient()
        client.force_login(self.test_user)

        original_number = '+6171234567'
        UserPhoneNumberDetails.objects.create(user=self.test_user, phone_number=original_number)
        response = client.get(self.url)
        self.assertEqual(response.data['phone_number'], original_number)

        updated_phone_number = '+16175555555'
        details = {
            'phone_number': updated_phone_number
        }

        response = client.post(self.url, data=details)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], updated_phone_number)

    def test_phone_number_nonsense_update(self):
        client = APIClient()
        client.force_login(self.test_user)

        details = {
            'phone_number': 'abcde'
        }

        response = client.post(self.url, data=details)
        self.assertEqual(response.status_code, 400)
