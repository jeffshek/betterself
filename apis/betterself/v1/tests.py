from django.test import TestCase
from rest_framework.test import APIClient

from betterself.users.tests.mixins.test_mixins import UsersTestsMixin

API_V1_VALID_GET_RESOURCES = [
    'supplements',
]
API_V1_URL = '/api/v1/{0}'


class APIv1Tests(TestCase, UsersTestsMixin):
    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.create_authenticated_user(cls.client)

        super().setUpClass()

    def test_fake_resources_404(self):
        url = API_V1_URL.format('fake_made_up_resource')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 404)

    def test_all_resources_have_valid_get(self):
        for resource in API_V1_VALID_GET_RESOURCES:
            url = API_V1_URL.format(resource)
            request = self.client.get(url)
            self.assertEqual(request.status_code, 200)
