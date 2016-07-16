from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory

API_V1_RESOURCES = [
    'supplements',
]
API_V1_URL = "/api/v1/{0}"


class APIv1Tests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = APIRequestFactory()
        cls.client = APIClient()
        super().setUpClass()

    def test_fake_resources_404(self):
        url = API_V1_URL.format("fake_made_up_resource")
        request = self.client.get(url)
        self.assertEqual(request.status_code, 404)

    def test_all_resources_have_valid_get(self):
        for resource in API_V1_RESOURCES:
            url = API_V1_URL.format(resource)
            request = self.client.get(url)
            self.assertEqual(request.status_code, 200)
