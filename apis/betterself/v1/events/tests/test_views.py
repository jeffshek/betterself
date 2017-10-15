import datetime
import json

import dateutil.parser
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.constants import DAILY_FREQUENCY, MONTHLY_FREQUENCY
from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from apis.betterself.v1.tests.mixins.test_get_requests import GetRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_post_requests import PostRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_put_requests import PUTRequestsTestsMixin
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from betterself.utils.date_utils import UTC_TZ, get_current_date_days_ago, get_current_date_months_ago
from constants import VERY_PRODUCTIVE_MINUTES_VARIABLE
from events.fixtures.factories import UserActivityFactory, UserActivityEventFactory
from events.fixtures.mixins import SupplementEventsFixturesGenerator, ProductivityLogFixturesGenerator, \
    UserActivityEventFixturesGenerator
from events.models import SupplementLog, DailyProductivityLog, UserActivity, UserActivityLog, SleepLog, \
    SupplementReminder
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement
from vendors.fixtures.mixins import VendorModelsFixturesGenerator

User = get_user_model()


class TestSupplementEvents(BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin, PUTRequestsTestsMixin):
    # python manage.py test apis.betterself.v1.events.tests.TestSupplementEvents
    TEST_MODEL = SupplementLog
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
        event = SupplementLog.objects.get(uuid=uuid)

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
        valid_filter_value = DailyProductivityLog.objects.filter(user=self.user_1).first().very_productive_time_minutes
        request_parameters = {'very_productive_time_minutes': valid_filter_value}
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

    def test_that_rolling_window_of_one_works(self):
        five_days_ago = get_current_date_days_ago(5)
        reported_very_productive_value = 0
        cumulative_window = 1

        params = {
            'start_date': five_days_ago.isoformat(),
            'cumulative_window': cumulative_window,
        }
        response = self.client.get(self.url, data=params)
        for k, v in response.data.items():
            parsed_date = dateutil.parser.parse(k)
            if parsed_date.date() == five_days_ago:
                reported_very_productive_value = v[VERY_PRODUCTIVE_MINUTES_VARIABLE]

        very_productive_time = DailyProductivityLog.objects.get(user=self.default_user, date=five_days_ago). \
            very_productive_time_minutes

        self.assertEqual(very_productive_time, reported_very_productive_value)

    def test_that_rolling_window_parameter_works(self):
        six_days_ago = get_current_date_days_ago(6)
        five_days_ago = get_current_date_days_ago(5)
        reported_very_productive_value = 0
        cumulative_window = 2

        # if rolling by 2, you expect the sum to be the 5th and 6th day combined
        params = {
            'start_date': six_days_ago.isoformat(),
            'cumulative_window': cumulative_window,
        }
        response = self.client.get(self.url, data=params)

        for k, v in response.data.items():
            parsed_date = dateutil.parser.parse(k)
            if parsed_date.date() == five_days_ago:
                reported_very_productive_value = v[VERY_PRODUCTIVE_MINUTES_VARIABLE]

        # sum up the two individual results to make sure the analytics is correct
        very_productive_time_list = DailyProductivityLog.objects.filter(user=self.default_user, date__lte=five_days_ago,
            date__gte=six_days_ago).values_list(
            VERY_PRODUCTIVE_MINUTES_VARIABLE, flat=True)
        expected_very_productive_time = sum(very_productive_time_list)

        self.assertEqual(reported_very_productive_value, expected_very_productive_time)

    def test_that_rolling_window_parameter_aggregates_beginning_of_series(self):
        six_days_ago = get_current_date_days_ago(6)
        reported_very_productive_value = 0
        cumulative_window = 2

        # if rolling by 2, you expect the sum to be the 5th and 6th day combined
        params = {
            'start_date': six_days_ago.isoformat(),
            'cumulative_window': cumulative_window,
        }
        response = self.client.get(self.url, data=params)

        for k, v in response.data.items():
            parsed_date = dateutil.parser.parse(k)
            if parsed_date.date() == six_days_ago:
                reported_very_productive_value = v[VERY_PRODUCTIVE_MINUTES_VARIABLE]

        window_start_date = six_days_ago - relativedelta(days=cumulative_window)

        # sum up the two individual results to make sure the analytics is correct
        very_productive_time_list = DailyProductivityLog.objects.filter(user=self.default_user, date__lte=six_days_ago,
            date__gt=window_start_date).values_list(
            VERY_PRODUCTIVE_MINUTES_VARIABLE, flat=True)

        expected_very_productive_time = sum(very_productive_time_list)

        self.assertEqual(reported_very_productive_value, expected_very_productive_time)

    def test_productivity_log_works_with_appending_start_and_end_dates(self):
        start_date = get_current_date_months_ago(12)

        params = {
            'start_date': start_date.isoformat(),
            'complete_date_range_in_daily_frequency': True,
        }

        response = self.client.get(self.url, data=params)
        response_amount = len(response.data.keys())
        productivity_logs = DailyProductivityLog.objects.filter(user=self.default_user).count()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(response_amount, productivity_logs)


class TestSupplementLogsViews(TestCase):
    """
    Test class that gets activity for one specific supplement
    """

    @classmethod
    def setUpTestData(cls):
        cls.default_user, _ = User.objects.get_or_create(username='default')
        builder = DemoHistoricalDataBuilder(cls.default_user)
        builder.create_historical_fixtures()

        supplement = Supplement.objects.filter(user=cls.default_user).first()
        supplement_uuid = str(supplement.uuid)
        cls.supplement = supplement
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

        supplement_events_value_query = SupplementLog.objects.filter(user=self.default_user,
            supplement=self.supplement).aggregate(
            total_sum=Sum('quantity'))
        supplement_events_value = supplement_events_value_query['total_sum']

        response_sum = sum(response.data.values())
        self.assertEqual(response_sum, supplement_events_value)

    def test_view_works_with_valid_frequency_parameters(self):
        response = self.client.get(self.url, data={'frequency': 'daily'})
        self.assertEqual(response.status_code, 200)

    def test_view_works_with_valid_frequency_parameters_2(self):
        response = self.client.get(self.url, data={'frequency': None})
        self.assertEqual(response.status_code, 200)

    def test_view_works_with_invalid_frequency_parameters(self):
        response = self.client.get(self.url, data={'frequency': 'THIS IS MADE UP'})
        self.assertEqual(response.status_code, 400)

    def test_assert_daily_frequency_is_less_than_no_aggregration(self):
        # A supplement history that is stacked daily should return in less results that something that hasn't been
        # aggregated. IE. If you drink Coffee 3x on Monday, that only results on 1 record, versus 3 individual records
        # for no aggregation
        response_no_aggregation = self.client.get(self.url, data={'frequency': None})

        # now filter with parameters between the start and end times
        queryset = SupplementLog.objects.filter(user=self.default_user).order_by('time')
        start_date = queryset.first().time.date()
        end_date = queryset.last().time.date()

        daily_response_kwargs = {
            'frequency': 'daily',
            'start_date': start_date,
            'end_date': end_date
        }
        response_daily_aggregation = self.client.get(self.url, data=daily_response_kwargs)

        self.assertGreater(len(response_no_aggregation.data), len(response_daily_aggregation.data))
        # err on the side of caution that a dataframe and not a series is being returned (in that case, it would be
        # where the results returned is just a count of 1
        self.assertGreater(len(response_daily_aggregation.data), 10)
        self.assertGreater(len(response_no_aggregation.data), 10)

    def test_that_start_date_will_return_complete_daily_index_even_if_no_values_exist(self):
        """
        An API Query with a start_date should always return data saying null if there is no data
        This logic ensures matching indices on the frontend
        """
        start_date = get_current_date_months_ago(6)
        non_existent_date = get_current_date_months_ago(-6)
        request_params = {
            'start_date': start_date,
            'frequency': 'daily',
            'complete_date_range_in_daily_frequency': True
        }
        response = self.client.get(self.url, data=request_params)

        # response.data.keys() is a list of isoformat strings (with timezones), but they always have the date
        # so a bit of laziness here, just check for the matching string
        start_date_in_response = any(start_date.isoformat() in x for x in response.data.keys())
        fake_date_in_response = any(non_existent_date.isoformat() in x for x in response.data.keys())

        self.assertTrue(start_date_in_response)
        self.assertFalse(fake_date_in_response)

    def test_validation_logic_to_prevent_mismatch_frequency_and_complete_date_ranges(self):
        request_params = {
            'frequency': None,
            'complete_date_range_in_daily_frequency': True
        }
        response = self.client.get(self.url, data=request_params)
        self.assertEqual(response.status_code, 400)

    def test_supplement_log_on_supplement_with_no_events(self):
        # delete all the supplements
        SupplementLog.objects.filter(supplement=self.supplement).delete()
        response = self.client.get(self.url, data={'frequency': 'daily'})

        self.assertEqual(response.status_code, 200)


class TestAggregatedSupplementLogViews(TestCase):
    """ Bunch of subpar tests """

    @classmethod
    def setUpTestData(cls):
        cls.default_user, _ = User.objects.get_or_create(username='default')
        builder = DemoHistoricalDataBuilder(cls.default_user)
        builder.create_historical_fixtures()

        supplement = Supplement.objects.filter(user=cls.default_user).first()
        supplement_uuid = str(supplement.uuid)
        cls.supplement = supplement
        cls.url = reverse('aggregate-supplement-log', args=[supplement_uuid])

        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(self.default_user)

    def test_daily_view(self):
        request_params = {
            'frequency': DAILY_FREQUENCY,
        }

        response = self.client.get(self.url, data=request_params)
        self.assertEqual(response.status_code, 200)

    def test_event_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_monthly_view_no_sleep_logs(self):
        SleepLog.objects.filter(user=self.default_user).delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_monthly_view_no_productivity_logs(self):
        DailyProductivityLog.objects.filter(user=self.default_user).delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_monthly_view_no_supplement_logs(self):
        SupplementLog.objects.filter(user=self.default_user).delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_monthly_view(self):
        request_params = {
            'frequency': MONTHLY_FREQUENCY,
        }
        response = self.client.get(self.url, data=request_params)
        self.assertEqual(response.status_code, 200)


class SupplementReminderViewsTests(BaseAPIv1Tests, PostRequestsTestsMixin):
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
        self.assertEqual(response.status_code, 403)

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
