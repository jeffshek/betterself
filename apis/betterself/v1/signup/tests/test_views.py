from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apis.betterself.v1.signup.tasks import create_demo_fixtures
from betterself.users.models import DemoUserLog
from events.models import UserActivity
from events.utils.default_events_builder import DEFAULT_ACTIVITIES, SPECIAL_ACTIVITIES
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

    def test_create_user_with_email(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'password': 'somepassword',
            'email': 'awesome-email@gmail.com'
        }

        response = self.client.post(self.create_url, data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)

        self.assertEqual(User.objects.count(), self.starting_user_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['token'], token.key)
        self.assertEqual(user.email, data['email'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_duplicate_email(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'password': 'somepassword',
            'email': 'awesome-email@gmail.com'
        }

        self.client.post(self.create_url, data, format='json')

        data['username'] = 'jimmy'

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, 201, response.data)

    def test_create_user_with_garbage_email(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'password': 'somepassword',
            'email': 'garbage'
        }

        self.client.post(self.create_url, data, format='json')

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, 400, response.data)
        self.assertTrue('email' in response.data)

    def test_create_user_with_timezone(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'password': 'somepassword',
            'timezone': 'America/New_York'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.data['username'], data['username'])
        self.assertFalse('password' in response.data)

        created_user = User.objects.get(username=data['username'])
        self.assertEqual(created_user.timezone, data['timezone'])

    def test_create_user_with_invalid_timezone(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'password': 'somepassword',
            'timezone': 'WILLY-WONKA'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        # if invalid, should contain error about timezone
        self.assertTrue('timezone' in response.data)

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
        expected_activities = len(DEFAULT_ACTIVITIES) + len(SPECIAL_ACTIVITIES)
        self.assertEqual(expected_activities, user_activities.count())

        user_supplements = Supplement.objects.filter(user=user)
        self.assertTrue(len(user_supplements) > 0)

    def test_creation_of_user_with_create_supplements_parameter(self):
        username = 'foobar'
        data = {
            'username': username,
            'password': 'fly-like-an-eagle',
            'supplements': 'potato,bacon'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        potato_count = Supplement.objects.filter(user=user, name__iexact='potato').count()
        bacon_count = Supplement.objects.filter(user=user, name__iexact='bacon').count()

        self.assertEqual(potato_count, 1)
        self.assertEqual(bacon_count, 1)

    def test_creation_of_user_with_just_one_supplement(self):
        username = 'foobar'
        data = {
            'username': username,
            'password': 'fly-like-an-eagle',
            'supplements': 'potato'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        potato_count = Supplement.objects.filter(user=user, name__iexact='potato').count()
        bacon_count = Supplement.objects.filter(user=user, name__iexact='bacon').count()

        self.assertEqual(potato_count, 1)
        self.assertEqual(bacon_count, 0)

    def test_creation_of_user_with_create_supplements_with_some_odd_spacing(self):
        username = 'foobar'
        data = {
            'username': username,
            'password': 'fly-like-an-eagle',
            'supplements': 'coffee,    sugar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        sugar_count = Supplement.objects.filter(user=user, name__iexact='sugar').count()

        self.assertEqual(sugar_count, 1)

    def test_creation_of_user_with_duplicate_supplement_names(self):
        username = 'foobar'
        data = {
            'username': username,
            'password': 'fly-like-an-eagle',
            'supplements': 'coffee,    coffee,coffee'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        supplement_count = Supplement.objects.filter(user=user, name__iexact='coffee').count()

        self.assertEqual(supplement_count, 1)

    def test_creation_of_user_with_number_supplement_names(self):
        username = 'foobar'
        data = {
            'username': username,
            'password': 'fly-like-an-eagle',
            'supplements': 'coffee,1,2,3,4,coffee'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        supplement_count = Supplement.objects.filter(user=user).count()

        # coffee is in twice, so total count is 5
        self.assertEqual(supplement_count, 5)


class DemoAccountsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create the first demo fixture so that views will rely on it
        create_demo_fixtures()

    def setUp(self):
        self.create_url = reverse('api-create-demo-user')

    def test_demo_user_creation(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 201, response.data)

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

    def test_creation_of_demo_user_is_next_one_that_gets_fetched(self):
        # call demo fixtures
        create_demo_fixtures()

        this_should_be_last_demo_user_created = User.objects.all().order_by('date_joined').last()
        last_demo_user = DemoUserLog.objects.all().order_by('created').last()

        self.assertEqual(last_demo_user.user, this_should_be_last_demo_user_created)

        response = self.client.get(self.create_url)
        data = response.data
        uuid = data['uuid']
        user = User.objects.get(uuid=uuid)

        self.assertEqual(last_demo_user.user, user)

    def test_no_demo_user_on_signup_page_will_work(self):
        DemoUserLog.objects.all().delete()

        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 201, response.data)


class UserViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = reverse('api-logged-in-user-details')
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='usain-bolt')
        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(username='usain-bolt')
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

    def test_user_logged_in_includes_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200, response.data)

        expected_token = Token.objects.get(user=self.user).key
        self.assertEqual(response.data['token'], expected_token)

    def test_not_logged_user_cant_access_nothing(self):
        client = APIClient()
        response = client.get(self.url)

        self.assertEqual(response.status_code, 403, response.data)


class TestEmailConfirmation(TestCase):
    def test_fake_confirmation_email_returns_200(self):
        data = {'key': 'random_key'}
        url = reverse('account_confirm_email', kwargs=data)

        client = APIClient()
        response = client.get(url)
        # even when the confirmation doesnt exist, django returns a 200
        # and will just say something about validation key has expired, etc
        self.assertEqual(response.status_code, 200)
