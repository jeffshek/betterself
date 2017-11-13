from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model

from apis.betterself.v1.tests.mixins.test_get_requests import GetRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_post_requests import PostRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_put_requests import PUTRequestsTestsMixin
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from betterself.utils.date_utils import get_current_utc_time_and_tz
from events.fixtures.factories import UserMoodLogFactory
from events.models import UserMoodLog

User = get_user_model()


class TestUserMoodLogViews(BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin, PUTRequestsTestsMixin):
    TEST_MODEL = UserMoodLog
    PAGINATION = True
    FIXTURES_SIZE = 50

    DEFAULT_POST_PARAMS = {
        'value': 5
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        now = get_current_utc_time_and_tz()
        for subtract_seconds in range(0, cls.FIXTURES_SIZE):
            time = now - relativedelta(seconds=subtract_seconds)
            UserMoodLogFactory(time=time, user=cls.user_1)

    def test_valid_get_request_with_params_filters_correctly(self):
        request_parameters = {'value': 1}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        key = 'value'
        super().test_valid_get_request_for_key_in_response(key)
