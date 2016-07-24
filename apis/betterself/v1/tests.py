from django.test import TestCase
from rest_framework.test import APIClient

from betterself.users.tests.mixins.test_mixins import UsersTestsMixin

VALID_GET_RESOURCES = [
    'supplements',
]
API_V1_URL = '/api/v1/{0}'


class APIv1Tests(TestCase, UsersTestsMixin):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.client = self.create_authenticated_user_on_client(APIClient(), self.user)

    def test_fake_resources_404(self):
        url = API_V1_URL.format('fake_made_up_resource')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 404)

    def test_all_resources_have_valid_get(self):
        for resource in VALID_GET_RESOURCES:
            url = API_V1_URL.format(resource)
            request = self.client.get(url)
            self.assertEqual(request.status_code, 200)
