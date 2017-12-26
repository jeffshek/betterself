import datetime
from dateutil.relativedelta import relativedelta

from apis.betterself.v1.tests.mixins.test_get_requests import GetRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_post_requests import PostRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_put_requests import PUTRequestsTestsMixin
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from events.fixtures.factories import UserActivityFactory, UserActivityEventFactory
from events.fixtures.mixins import UserActivityEventFixturesGenerator
from events.models import UserActivity, UserActivityLog


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
