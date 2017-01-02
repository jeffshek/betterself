import datetime
import json

from django.contrib.auth import get_user_model

from apis.betterself.v1.tests.test_base import BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from events.fixtures.mixins import EventModelsFixturesGenerator
from events.models import SupplementEvent
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement
from vendors.fixtures.mixins import VendorModelsFixturesGenerator

User = get_user_model()


class TestSupplementEvents(BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin):
    # python manage.py test apis.betterself.v1.events.tests.TestSupplementEvents
    TEST_MODEL = SupplementEvent

    def setUp(self):
        defaults_user, _ = User.objects.get_or_create(username='default')
        self.DEFAULT_POST_PARAMS = {
            'time': datetime.datetime.now().isoformat(),
            'quantity': 5,
            'source': 'api',
            'user': str(defaults_user.uuid)
        }

        # pass a parameter just to make sure the default parameter is valid
        valid_supplement = Supplement.get_user_viewable_objects(self.user_1).first()
        self.DEFAULT_POST_PARAMS['supplement_uuid'] = str(valid_supplement.uuid)

        super().setUp()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        SupplementModelsFixturesGenerator.create_fixtures()
        VendorModelsFixturesGenerator.create_fixtures()
        EventModelsFixturesGenerator.create_fixtures(cls.user_1)

    def test_default_parameters_created_correctly(self):
        # a bit too much of an integration test, but realized that
        # it was overly friendly and tests were passing without catching
        # potential issues
        self._make_post_request(self.client_1, self.DEFAULT_POST_PARAMS)

    def test_valid_get_request_for_key_in_response(self):
        request_parameters = {'quantity': 1}
        key = 'quantity'
        super().test_valid_get_request_for_key_in_response(request_parameters, key)

    def test_valid_get_request_with_params(self):
        request_parameters = {'quantity': 5.0}
        super().test_valid_get_request_with_params(request_parameters)

    def test_event_invalid_supplement_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        now = datetime.datetime.now()
        now = now.isoformat()

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
