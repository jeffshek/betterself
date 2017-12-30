import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.tests.mixins.test_get_requests import GetRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_post_requests import PostRequestsTestsMixin
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from betterself.utils.date_utils import UTC_TZ, get_current_utc_time_and_tz
from events.fixtures.mixins import UserSupplementStackFixturesGenerator
from events.models import SupplementLog, SleepLog
from supplements.models import UserSupplementStack

User = get_user_model()


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
