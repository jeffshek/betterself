import datetime
import json

from apis.betterself.v1.tests.test_base import BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from events.fixtures.mixins import EventModelsFixturesGenerator
from events.models import SupplementEvent
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement
from vendors.fixtures.mixins import VendorModelsFixturesGenerator


class TestSupplementEvents(BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin):
    TEST_MODEL = SupplementEvent

    def setUp(self):
        self.DEFAULT_POST_PARAMS = {
            'time': datetime.datetime.now().isoformat(),
            'quantity': 5,
            'source': 'api',
        }
        super().setUp()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        SupplementModelsFixturesGenerator.create_fixtures()
        VendorModelsFixturesGenerator.create_fixtures()
        EventModelsFixturesGenerator.create_fixtures(cls.user_1)

        # pass a parameter just to make sure the default parameter is valid
        valid_supplement = Supplement.get_user_viewable_objects(cls.user_1).first()
        cls.DEFAULT_POST_PARAMS['supplement_product_id'] = valid_supplement.id

    def test_valid_get_request_for_key_in_response(self):
        request_parameters = {'quantity': 1}
        key = 'quantity'
        super().test_valid_get_request_for_key_in_response(request_parameters, key)

    def test_valid_get_request_with_params(self):
        request_parameters = {'quantity': 'Glutamine'}
        super().test_valid_get_request_with_params(request_parameters)

    def test_event_invalid_supplement_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        now = datetime.datetime.now()
        now = now.isoformat()

        # negative ids don't exist ... so this should fail
        data = {
            'supplement_product_id': -1,
            'time': now,
        }

        data = json.dumps(data)
        request = self.client_1.post(url, data, content_type='application/json')
        self.assertEqual(request.status_code, 400)

    def test_uniqueness_on_post_requests(self):
        request = self._make_post_request(self.client_1, self.DEFAULT_POST_PARAMS)
        self.assertEqual(request.status_code, 201)
