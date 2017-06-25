from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from betterself.users.models import DemoUserLog
from events.models import UserActivity
from events.utils.default_events_builder import DEFAULT_ACTIVITIES
from supplements.models import Supplement

User = get_user_model()


# thanks to https://github.com/iheanyi/ for writing the initial group of these


class AccountsTest(TestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'testpassword')

        # URL for creating an account.
        self.create_url = reverse('api-create-user')
        self.starting_user_count = User.objects.count()

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'password': 'somepassword'
        }

        response = self.client.post(self.create_url, data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(User.objects.count(), self.starting_user_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['token'], token.key)
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        """
        Ensures user is not created for password lengths less than 8.
        """

        data = {
            'username': 'foobar',
            'password': 'foo'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.starting_user_count)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
            'username': 'foobar',
            'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.starting_user_count)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'foo' * 30,
            'password': 'foobar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.starting_user_count)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
            'username': '',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.starting_user_count)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
            'username': 'testuser',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.starting_user_count)
        self.assertEqual(len(response.data['username']), 1)

    def test_creating_new_user_creates_defaults(self):
        username = 'a-brand-new-world'
        data = {
            'username': username,
            'password': 'a-brand-new-world'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=username)

        # check that the defaults for user-activities exist after being created
        user_activities = UserActivity.objects.filter(user=user)
        self.assertEqual(len(DEFAULT_ACTIVITIES), user_activities.count())

        user_supplements = Supplement.objects.filter(user=user)
        self.assertTrue(len(user_supplements) > 0)


class DemoAccountsTest(TestCase):
    def setUp(self):
        self.create_url = reverse('api-create-demo-user')

    def test_demo_user_creation(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 201)

    def test_demo_user_creation_is_in_demo_user_log(self):
        response = self.client.get(self.create_url)
        data = response.data

        uuid = data['uuid']
        user = User.objects.get(uuid=uuid)

        demo_user_log = DemoUserLog.objects.get(user=user)
        self.assertEqual(demo_user_log.user, user)

    def test_delete_demo_user_log_deletes_user(self):
        response = self.client.get(self.create_url)
        data = response.data

        uuid = data['uuid']
        user = User.objects.get(uuid=uuid)

        demo_user_log = DemoUserLog.objects.get(user=user)
        demo_user_log.delete()

        user_matching_deleted_uuid = User.objects.filter(uuid=uuid).count()
        self.assertEqual(user_matching_deleted_uuid, 0)


class UserViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = reverse('api-logged-in-user-details')
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='usain-bolt')
        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_deleting_of_user(self):
        # first let's make sure the user exists in db
        test_user_exists = User.objects.filter(username=self.user.username).exists()
        self.assertTrue(test_user_exists)

        # send to the right view to make sure what we expect is removed
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 202)

        test_user_exists_second = User.objects.filter(username=self.user.username).exists()
        self.assertFalse(test_user_exists_second)

    def test_user_logged_in_details_correct(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        username = response.data['username']
        uuid = response.data['uuid']

        self.assertEqual(self.user.username, username)
        self.assertEqual(str(self.user.uuid), uuid)
