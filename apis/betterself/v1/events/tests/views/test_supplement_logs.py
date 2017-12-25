import datetime
import json

import dateutil.parser
from django.db.models import Sum
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.constants import DAILY_FREQUENCY, MONTHLY_FREQUENCY
from apis.betterself.v1.events.tests.views.test_views import User
from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder

from apis.betterself.v1.tests.mixins.test_get_requests import GetRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_post_requests import PostRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_put_requests import PUTRequestsTestsMixin
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from betterself.utils.date_utils import get_current_date_months_ago
from events.fixtures.mixins import SupplementEventsFixturesGenerator
from events.models import SupplementLog, SleepLog, DailyProductivityLog
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement
from vendors.fixtures.mixins import VendorModelsFixturesGenerator


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
