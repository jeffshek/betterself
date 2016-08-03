import json
from django.test import TestCase
from rest_framework.test import APIClient

from betterself.users.tests.mixins.test_mixins import UsersTestsMixin
from supplements.fixtures.factories import IngredientFactory
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement, IngredientComposition
from vendors.fixtures.factories import DEFAULT_VENDOR_NAME
from vendors.fixtures.mixins import VendorModelsFixturesGenerator
from vendors.models import Vendor

VALID_GET_RESOURCES = [
    Supplement.RESOURCE_NAME,
]

API_V1_LIST_CREATE_URL = '/api/v1/{0}'


class APIv1Tests(TestCase, UsersTestsMixin):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.ingredient = IngredientFactory()

        # generic fixtures based on the apps, inclusive of models
        # like measurement objects
        SupplementModelsFixturesGenerator.create_fixtures()
        VendorModelsFixturesGenerator.create_fixtures()

    def setUp(self):
        self.client = self.create_authenticated_user_on_client(APIClient(), self.user)

    def test_fake_resources_404(self):
        url = API_V1_LIST_CREATE_URL.format('fake_made_up_resource')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 404)

    def test_all_resources_have_valid_get(self):
        for resource in VALID_GET_RESOURCES:
            url = API_V1_LIST_CREATE_URL.format(resource)
            request = self.client.get(url)
            self.assertEqual(request.status_code, 200)

    def test_supplement_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(Supplement.RESOURCE_NAME)
        request = self.client.get(url)

        self.assertEqual(request.status_code, 200)

    def test_supplement_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(Supplement.RESOURCE_NAME)
        request_parameters = {
            'name': 'Glutamine',
            'vendor_id': 2,
            'ingredient_compositions_ids': '1,2'  # this should probably be CSV enforced
        }
        data = json.dumps(request_parameters)
        request = self.client.post(url, data=data, content_type='application/json')

        self.assertEqual(request.status_code, 201)

    def test_vendor_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(Vendor.RESOURCE_NAME)
        request_parameters = {
            'name': 'Advil',
            'email': 'advil@advil.com',
            'url:': 'advil.com',
        }
        data = json.dumps(request_parameters)
        request = self.client.post(url, data=data, content_type='application/json')

        self.assertEqual(request.status_code, 201)

    def test_vendor_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(Vendor.RESOURCE_NAME)
        request = self.client.get(url)

        self.assertEqual(request.status_code, 200)
        vendor_names = [item['name'] for item in request.data]

        # we made a default vendor, so that should definitely be in here
        self.assertTrue(DEFAULT_VENDOR_NAME in vendor_names)

    def test_ingredient_composition_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(IngredientComposition.RESOURCE_NAME)
        request = self.client.get(url)

        self.assertEqual(request.status_code, 200)

    def test_ingredient_composition_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(IngredientComposition.RESOURCE_NAME)

        request_parameters = {
            'ingredient_id': '1',
            'measurement_id': '1',
            'quantity:': '5.0',
        }
        data = json.dumps(request_parameters)
        request = self.client.post(url, data=data, content_type='application/json')

        self.assertEqual(request.status_code, 200)
