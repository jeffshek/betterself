from apis.betterself.v1.constants import VALID_REST_RESOURCES
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL


class GeneralAPIv1Tests(BaseAPIv1Tests):
    def test_fake_resources_404(self):
        url = API_V1_LIST_CREATE_URL.format('fake_made_up_resource')
        request = self.client_1.get(url)
        self.assertEqual(request.status_code, 404)

    def test_all_resources_have_valid_get(self):
        for resource in VALID_REST_RESOURCES:
            resource_name = resource.RESOURCE_NAME

            url = API_V1_LIST_CREATE_URL.format(resource_name)
            request = self.client_1.get(url)
            self.assertEqual(request.status_code, 200)

    def test_all_resources_have_resource_name(self):
        for resource in VALID_REST_RESOURCES:
            has_resource_name = getattr(resource, 'RESOURCE_NAME')
            self.assertTrue(has_resource_name)
