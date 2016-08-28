import logging

from apis.betterself.v1.tests.test_base import BaseAPIv1Tests, VALID_GET_RESOURCES, logger
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL

logger.setLevel(logging.ERROR)


class GeneralAPIv1Tests(BaseAPIv1Tests):
    def test_fake_resources_404(self):
        url = API_V1_LIST_CREATE_URL.format('fake_made_up_resource')
        request = self.client_1.get(url)
        self.assertEqual(request.status_code, 404)

    def test_all_resources_have_valid_get(self):
        for resource in VALID_GET_RESOURCES:
            url = API_V1_LIST_CREATE_URL.format(resource)
            request = self.client_1.get(url)
            self.assertEqual(request.status_code, 200)
