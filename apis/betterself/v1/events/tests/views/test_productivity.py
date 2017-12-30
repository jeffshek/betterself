import datetime

import dateutil.parser
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.events.tests.views.test_views import User
from apis.betterself.v1.tests.mixins.test_get_requests import GetRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_post_requests import PostRequestsTestsMixin
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from betterself.utils.date_utils import get_current_date_days_ago, get_current_date_months_ago
from constants import VERY_PRODUCTIVE_MINUTES_VARIABLE
from events.fixtures.mixins import ProductivityLogFixturesGenerator
from events.models import DailyProductivityLog


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
        self.assertEqual(response.status_code, 401)

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
