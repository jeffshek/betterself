import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from apis.betterself.v1.tests.mixins.test_get_requests import GetRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_post_requests import PostRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_put_requests import PUTRequestsTestsMixin
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from betterself.utils.date_utils import UTC_TZ, get_current_utc_time_and_tz
from events.fixtures.factories import UserActivityFactory, UserActivityEventFactory
from events.fixtures.mixins import UserActivityEventFixturesGenerator, UserSupplementStackFixturesGenerator
from events.models import SupplementLog, UserActivity, UserActivityLog, SleepLog, \
    SupplementReminder
from supplements.models import Supplement, UserSupplementStack

User = get_user_model()


class TestUserActivityViews(BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin, PUTRequestsTestsMixin):
    TEST_MODEL = UserActivity
    PAGINATION = True
    DEFAULT_POST_PARAMS = {
        'name': 'Went For A Run',
        'is_significant_activity': True
    }
    SECONDARY_ACTIVITY_NAME = 'Had Breakfast'
    SECONDARY_POST_PARAMS = {
        'name': SECONDARY_ACTIVITY_NAME,
        'is_significant_activity': False
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        UserActivityEventFixturesGenerator.create_fixtures(cls.user_1)
        UserActivityFactory(user=cls.user_1, **cls.SECONDARY_POST_PARAMS)

    def test_valid_get_request_for_key_in_response(self):
        key = 'name'
        super().test_valid_get_request_for_key_in_response(key)

    def test_valid_get_request_with_params_filters_correctly(self):
        request_parameters = {'name': self.SECONDARY_ACTIVITY_NAME}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)


class TestUserActivityEventViews(BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin, PUTRequestsTestsMixin):
    TEST_MODEL = UserActivityLog
    PAGINATION = True

    def setUp(self):
        current_time = datetime.datetime.now()
        previous_time = current_time - relativedelta(days=5)
        self.DEFAULT_POST_PARAMS = {
            'time': previous_time.isoformat(),
            'source': 'user_excel',
            'duration_minutes': 30
        }

        # pass a parameter just to make sure the default parameter is valid
        self.valid_user_activity = UserActivity.objects.filter(user=self.user_1).first()
        self.DEFAULT_POST_PARAMS['user_activity_uuid'] = str(self.valid_user_activity.uuid)

        super().setUp()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        UserActivityEventFixturesGenerator.create_fixtures(cls.user_1)

    def test_valid_get_request_for_key_in_response(self):
        key = 'duration_minutes'
        super().test_valid_get_request_for_key_in_response(key)

    def test_valid_get_request_with_params_filters_correctly(self):
        UserActivityEventFactory(user=self.user_1, duration_minutes=30)
        request_parameters = {'duration_minutes': 30}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)


class TestSleepActivityViews(BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin):
    # python manage.py test apis.betterself.v1.events.tests.TestSleepActivityViews
    TEST_MODEL = SleepLog
    PAGINATION = True

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # create a sleep record for two days
        start_time = datetime.datetime(2017, 1, 1, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2017, 1, 1, hour=7, tzinfo=UTC_TZ)
        SleepLog.objects.create(user=cls.user_1, start_time=start_time, end_time=end_time)
        # day two
        start_time = datetime.datetime(2017, 1, 2, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2017, 1, 2, hour=7, tzinfo=UTC_TZ)
        SleepLog.objects.create(user=cls.user_1, start_time=start_time, end_time=end_time)

    def setUp(self):
        start_time = datetime.datetime.utcnow() - relativedelta(hours=8)
        self.DEFAULT_POST_PARAMS = {
            'start_time': start_time.isoformat(),
            'end_time': datetime.datetime.utcnow().isoformat(),
            'source': 'api',
        }

        super().setUp()

    def test_post_request(self):
        post_parameters = self.DEFAULT_POST_PARAMS

        # multiple users should be able to create the same object
        request = self._make_post_request(self.client_1, post_parameters)
        self.assertEqual(request.status_code, 201, request.data)

        second_request = self._make_post_request(self.client_2, post_parameters)
        self.assertEqual(second_request.status_code, 201, second_request.data)

        # # now let's make sure that different users should be accessing different objects
        client_1_objects_count = self.TEST_MODEL.objects.filter(user=self.user_1).count()
        client_2_objects_count = self.TEST_MODEL.objects.filter(user=self.user_2).count()

        self.assertTrue(client_1_objects_count > 0)
        self.assertTrue(client_2_objects_count > 0)

    def test_valid_get_request_for_key_in_response(self):
        key = 'start_time'
        super().test_valid_get_request_for_key_in_response(key)

    def test_valid_get_request_with_params_filters_correctly(self):
        end_time = datetime.datetime(2017, 1, 1, hour=7, tzinfo=datetime.timezone.utc).astimezone()
        end_time_iso = end_time.isoformat()

        request_parameters = {'end_time': end_time_iso}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)

    def test_post_with_invalid_time_returns_400(self):
        """ in here the start_time is equivalent to end_time which is a no no """
        end_time = datetime.datetime(2017, 1, 1, hour=7, tzinfo=datetime.timezone.utc).astimezone()
        end_time_iso = end_time.isoformat()
        start_time_iso = end_time.isoformat()

        request_parameters = {
            'start_time': start_time_iso,
            'end_time': end_time_iso
        }

        response = self._make_post_request(self.client_1, request_parameters)
        self.assertEqual(response.status_code, 400)

    def test_post_with_invalid_start_time_returns_400(self):
        """ in here the start_time is after the end_time which is a no no """
        start_time = datetime.datetime(2017, 1, 2, hour=7, tzinfo=datetime.timezone.utc).astimezone()
        end_time = datetime.datetime(2017, 1, 1, hour=7, tzinfo=datetime.timezone.utc).astimezone()
        end_time_iso = end_time.isoformat()
        start_time_iso = start_time.isoformat()

        request_parameters = {
            'start_time': start_time_iso,
            'end_time': end_time_iso
        }

        response = self._make_post_request(self.client_1, request_parameters)
        self.assertEqual(response.status_code, 400, response.data)

    def test_post_with_valid_time_returns_200(self):
        start_time = datetime.datetime(2017, 12, 1, hour=7, tzinfo=datetime.timezone.utc).astimezone()
        end_time = datetime.datetime(2017, 12, 2, hour=7, tzinfo=datetime.timezone.utc).astimezone()
        end_time_iso = end_time.isoformat()
        start_time_iso = start_time.isoformat()

        request_parameters = {
            'start_time': start_time_iso,
            'end_time': end_time_iso,
            'source': 'api'
        }

        response = self._make_post_request(self.client_1, request_parameters)
        self.assertEqual(response.status_code, 201, response.data)

    def test_post_with_overlapping_valid_time_returns_400(self):
        start_time = datetime.datetime(2017, 1, 1, hour=7, tzinfo=datetime.timezone.utc).astimezone()
        end_time = datetime.datetime(2017, 1, 2, hour=7, tzinfo=datetime.timezone.utc).astimezone()
        end_time_iso = end_time.isoformat()
        start_time_iso = start_time.isoformat()

        request_parameters = {
            'start_time': start_time_iso,
            'end_time': end_time_iso,
            'source': 'api'
        }

        response = self._make_post_request(self.client_1, request_parameters)
        self.assertEqual(response.status_code, 400, response.data)


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


class TestUserStackRecordView(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        User = get_user_model()
        cls.default_user, _ = User.objects.get_or_create(username='user-stack-testing')
        UserSupplementStackFixturesGenerator.create_fixtures(cls.default_user)
        cls.url = reverse('record-supplement-stack')

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(self.default_user)

    def test_stack_record_view(self):
        stack = UserSupplementStack.objects.all().first()
        data = {
            'stack_uuid': str(stack.uuid)
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, 201, response.data)

    def test_stack_record_events_correctly(self):
        original_log_count = SupplementLog.objects.filter(user=self.default_user).count()

        stack = UserSupplementStack.objects.all().first()
        data = {
            'stack_uuid': str(stack.uuid)
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, 201, response.data)

        expected_log_size = original_log_count + stack.compositions.count()
        updated_log_count = SupplementLog.objects.filter(user=self.default_user).count()
        self.assertEqual(expected_log_size, updated_log_count)

    def test_stack_record_log_records_will_not_duplicate(self):
        original_log_count = SupplementLog.objects.filter(user=self.default_user).count()

        stack = UserSupplementStack.objects.all().first()
        data = {
            'stack_uuid': str(stack.uuid),
            'time': get_current_utc_time_and_tz().isoformat()
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, 201, response.data)

        # now post this multiple times to make sure won't duplicate
        self.client.post(self.url, data=data, format='json')
        self.client.post(self.url, data=data, format='json')

        expected_log_size = original_log_count + stack.compositions.count()
        updated_log_count = SupplementLog.objects.filter(user=self.default_user).count()
        self.assertEqual(expected_log_size, updated_log_count)

    def test_invalid_stack_record_view(self):
        data = {
            'stack_uuid': '1234'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, 400, response.data)
