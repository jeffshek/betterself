import datetime
import json

import dateutil.parser
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIClient

from apis.betterself.v1.events.serializers import valid_daily_max_minutes
from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from apis.betterself.v1.tests.mixins.test_get_requests import GetRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_post_requests import PostRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_put_requests import PUTRequestsTestsMixin
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from betterself.utils.date_utils import UTC_TZ, get_current_date_days_ago
from events.fixtures.factories import UserActivityFactory, UserActivityEventFactory
from events.fixtures.mixins import SupplementEventsFixturesGenerator, ProductivityLogFixturesGenerator, \
    UserActivityEventFixturesGenerator
from events.models import SupplementEvent, DailyProductivityLog, UserActivity, UserActivityEvent, SleepActivity
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement
from vendors.fixtures.mixins import VendorModelsFixturesGenerator

User = get_user_model()


# python manage.py test apis.betterself.v1.events.tests

class TestSerializerUtils(TestCase):
    @staticmethod
    def test_regular_max_minutes():
        valid_daily_max_minutes(600)

    def test_more_than_daily_max_minutes(self):
        with self.assertRaises(serializers.ValidationError):
            valid_daily_max_minutes(3601)

    def test_less_than_zero_max_minutes(self):
        with self.assertRaises(serializers.ValidationError):
            valid_daily_max_minutes(-50)


class TestSupplementEvents(BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin, PUTRequestsTestsMixin):
    # python manage.py test apis.betterself.v1.events.tests.TestSupplementEvents
    TEST_MODEL = SupplementEvent
    PAGINATION = True

    def setUp(self):
        self.DEFAULT_POST_PARAMS = {
            'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'quantity': 5,
            'source': 'api',
        }

        # pass a parameter just to make sure the default parameter is valid
        valid_supplement = Supplement.objects.filter(user=self.user_1).first()
        self.DEFAULT_POST_PARAMS['supplement_uuid'] = str(valid_supplement.uuid)

        super().setUp()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        SupplementModelsFixturesGenerator.create_fixtures()
        VendorModelsFixturesGenerator.create_fixtures()
        SupplementEventsFixturesGenerator.create_fixtures(cls.user_1)

    def test_default_parameters_created_correctly(self):
        # this is a bit too much of an integration test, but realized that
        # it was overly friendly and tests were passing without catching
        # potential issues
        params_time = dateutil.parser.parse(self.DEFAULT_POST_PARAMS['time'])
        quantity = self.DEFAULT_POST_PARAMS['quantity']
        source = self.DEFAULT_POST_PARAMS['source']
        user = self.user_1

        response = self._make_post_request(self.client_1, self.DEFAULT_POST_PARAMS)
        uuid = response.data['uuid']
        event = SupplementEvent.objects.get(uuid=uuid)

        event_time = event.time
        self.assertEqual(params_time.microsecond, event_time.microsecond)
        self.assertEqual(quantity, event.quantity)
        self.assertEqual(source, event.source)
        self.assertEqual(user, event.user)

    def test_valid_get_request_for_key_in_response(self):
        key = 'quantity'
        super().test_valid_get_request_for_key_in_response(key)

    def test_valid_get_request_with_params_filters_correctly(self):
        request_parameters = {'quantity': 4.0}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)

    def test_event_invalid_supplement_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        now = datetime.datetime.now().isoformat()

        # negative ids don't exist ... so this should fail
        data = {
            'supplement_uuid': -1,
            'time': now,
        }

        data = json.dumps(data)
        request = self.client_1.post(url, data, content_type='application/json')
        self.assertEqual(request.status_code, 400)

    def test_uniqueness_on_post_requests(self):
        """
        See how many objects were originally, make a request, and then see if it remains the same after
        posting the same data. It should!
        """
        amount_of_events = self.TEST_MODEL.objects.filter(user=self.user_1).count()

        self._make_post_request(self.client_1, self.DEFAULT_POST_PARAMS)
        amount_of_events_post_request = self.TEST_MODEL.objects.filter(user=self.user_1).count()

        self._make_post_request(self.client_1, self.DEFAULT_POST_PARAMS)
        amount_of_events_post_request_repeated = self.TEST_MODEL.objects.filter(user=self.user_1).count()

        self.assertTrue(amount_of_events_post_request > amount_of_events)
        self.assertEqual(amount_of_events_post_request_repeated, amount_of_events_post_request)


class TestProductivityLogViews(BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin):
    # python manage.py test apis.betterself.v1.events.tests.TestProductivityLogViews
    TEST_MODEL = DailyProductivityLog
    PAGINATION = True

    def setUp(self):
        self.DEFAULT_POST_PARAMS = {
            'date': datetime.date.today().isoformat(),
            'very_productive_time_minutes': 10,
            'source': 'api',
        }
        super().setUp()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        ProductivityLogFixturesGenerator.create_fixtures(cls.user_1)

    def test_valid_get_request_for_key_in_response(self):
        key = 'very_productive_time_minutes'
        super().test_valid_get_request_for_key_in_response(key)

    def test_valid_get_request_with_params_filters_correctly(self):
        request_parameters = {'very_productive_time_minutes': 10}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)


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
    TEST_MODEL = UserActivityEvent
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
    TEST_MODEL = SleepActivity
    PAGINATION = True

    def setUp(self):
        start_time = datetime.datetime.utcnow() - relativedelta(hours=8)
        self.DEFAULT_POST_PARAMS = {
            'start_time': start_time.isoformat(),
            'end_time': datetime.datetime.utcnow().isoformat(),
            'source': 'api',
        }

        super().setUp()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # create a sleep record for two days
        start_time = datetime.datetime(2017, 1, 1, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2017, 1, 1, hour=7, tzinfo=UTC_TZ)
        SleepActivity.objects.create(user=cls.user_1, start_time=start_time, end_time=end_time)
        # day two
        start_time = datetime.datetime(2017, 1, 2, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2017, 1, 2, hour=7, tzinfo=UTC_TZ)
        SleepActivity.objects.create(user=cls.user_1, start_time=start_time, end_time=end_time)

    def test_valid_get_request_for_key_in_response(self):
        key = 'start_time'
        super().test_valid_get_request_for_key_in_response(key)

    def test_valid_get_request_with_params_filters_correctly(self):
        end_time = datetime.datetime(2017, 1, 1, hour=7, tzinfo=datetime.timezone.utc).astimezone()
        end_time_iso = end_time.isoformat()

        request_parameters = {'end_time': end_time_iso}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)


class TestAggregateProductivityViews(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = reverse('productivity-aggregates')
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.default_user, _ = User.objects.get_or_create(username='default')
        ProductivityLogFixturesGenerator.create_fixtures_starting_from_today(cls.default_user, periods_back=60)
        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(self.default_user)

    def test_view_without_passing_parameters(self):
        response = self.client.get(self.url)
        data = response.data
        self.assertEqual(len(data), DailyProductivityLog.objects.filter(user=self.default_user).count())
        self.assertEqual(response.status_code, 200)

    def test_view_without_login(self):
        not_logged_in_client = APIClient()
        response = not_logged_in_client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_with_user_and_no_data(self):
        client = APIClient()
        new_user, _ = User.objects.get_or_create(username='new-user')
        client.force_login(new_user)

        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_with_start_date(self):
        five_days_ago = get_current_date_days_ago(5)
        six_days_ago = get_current_date_days_ago(6)

        params = {
            'start_date': five_days_ago.isoformat()
        }
        response = self.client.get(self.url, data=params)

        data = response.data
        dates = list(data.keys())
        dates_serialized = [dateutil.parser.parse(x).date() for x in dates]

        self.assertIn(five_days_ago, dates_serialized)
        self.assertNotIn(six_days_ago, dates_serialized)


class SupplementLogsTest(TestCase):
    """ Test class that gets activity for one specific supplement
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.default_user, _ = User.objects.get_or_create(username='default')
        builder = DemoHistoricalDataBuilder(cls.default_user)
        builder.create_historical_fixtures()

        supplement = Supplement.objects.filter(user=cls.default_user).first()
        supplement_uuid = str(supplement.uuid)

        cls.url = reverse('supplement-log', args=[supplement_uuid])

        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(self.default_user)

    def test_basic_view_functionality_with_invalid_url_returns_nothing(self):
        url = reverse('supplement-log', args=['cat'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404, response.data)

    def test_view_works(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_works_with_valid_frequency_parameters(self):
        response = self.client.get(self.url, data={'frequency': 'daily'})
        self.assertEqual(response.status_code, 200)

    def test_view_works_with_valid_frequency_parameters_2(self):
        response = self.client.get(self.url, data={'frequency': None})
        self.assertEqual(response.status_code, 200)

    def test_view_works_with_invalid_frequency_parameters(self):
        response = self.client.get(self.url, data={'frequency': 'THIS IS MADE UP'})
        self.assertEqual(response.status_code, 400)
