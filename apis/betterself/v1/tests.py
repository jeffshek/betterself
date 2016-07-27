from django.test import TestCase
from rest_framework.test import APIClient

from betterself.users.tests.mixins.test_mixins import UsersTestsMixin
from supplements.fixtures.factories import IngredientFactory
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement

VALID_GET_RESOURCES = [
    Supplement.RESOURCE_NAME,
]
API_V1_URL = '/api/v1/{0}'


class APIv1Tests(TestCase, UsersTestsMixin):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.ingredient = IngredientFactory()
        SupplementModelsFixturesGenerator.create_factory_fixtures()

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

    def test_supplement_get_request(self):
        url = API_V1_URL.format(Supplement.RESOURCE_NAME)
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)
