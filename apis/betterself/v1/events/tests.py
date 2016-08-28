import datetime
import json

from apis.betterself.v1.tests import BaseAPIv1Tests
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from events.fixtures.mixins import EventModelsFixturesGenerator
from events.models import SupplementEvent
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement
from vendors.fixtures.mixins import VendorModelsFixturesGenerator


class TestSupplementEvents(BaseAPIv1Tests):
    TEST_MODEL = SupplementEvent

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        SupplementModelsFixturesGenerator.create_fixtures()
        VendorModelsFixturesGenerator.create_fixtures()
        EventModelsFixturesGenerator.create_fixtures(cls.user_1)

    def test_event_valid_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)
        self.assertEqual(request.status_code, 200)

    def test_event_empty_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.post(url)
        self.assertEqual(request.status_code, 400)

    def test_event_valid_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        now = datetime.datetime.now()
        now = now.isoformat()

        # get the first viewable supplement
        viewable_supplement_id = Supplement.get_user_viewable_objects(self.user_1).first().id

        data = {
            'supplement_product_id': viewable_supplement_id,
            'time': now,
        }

        data = json.dumps(data)
        request = self.client_1.post(url, data, content_type='application/json')
        self.assertEqual(request.status_code, 201)

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
