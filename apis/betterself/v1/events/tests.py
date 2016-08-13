from apis.betterself.v1.tests import BaseAPIv1Tests
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from events.models import SupplementEvent


class TestSupplementEvents(BaseAPIv1Tests):
    TEST_MODEL = SupplementEvent

    def test_event_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.get(url)

        self.assertEqual(request.status_code, 200)
