import json
import logging
from django.test import TestCase
from rest_framework.test import APIClient

from betterself.users.tests.mixins.test_mixins import UsersTestsMixin
from supplements.fixtures.factories import IngredientFactory
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement, IngredientComposition, Ingredient
from vendors.fixtures.factories import DEFAULT_VENDOR_NAME
from vendors.fixtures.mixins import VendorModelsFixturesGenerator
from vendors.models import Vendor

logger = logging.Logger(__name__)
logger.setLevel(logging.ERROR)

VALID_GET_RESOURCES = [
    Supplement.RESOURCE_NAME,
]

API_V1_LIST_CREATE_URL = '/api/v1/{0}'


class BaseAPIv1Tests(TestCase, UsersTestsMixin):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.ingredient = IngredientFactory()

        # generic fixtures based on the apps, inclusive of models
        # like measurement objects
        SupplementModelsFixturesGenerator.create_fixtures()
        VendorModelsFixturesGenerator.create_fixtures()

    def setUp(self):
        # user has to be authenticated per each test!
        self.client = self.create_authenticated_user_on_client(APIClient(), self.user)

    @staticmethod
    def _debug_request(request):
        """ Helper function that outputs everything for easier reading """
        logger.error('\n***Debugging Request***')
        logger.error(request.data)
        logger.error(request.status_code)


class GeneralAPIv1Tests(BaseAPIv1Tests):
    def test_fake_resources_404(self):
        url = API_V1_LIST_CREATE_URL.format('fake_made_up_resource')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 404)

    def test_all_resources_have_valid_get(self):
        for resource in VALID_GET_RESOURCES:
            url = API_V1_LIST_CREATE_URL.format(resource)
            request = self.client.get(url)
            self.assertEqual(request.status_code, 200)


class SupplementV1Tests(BaseAPIv1Tests):
    TEST_MODEL = Supplement

    def test_supplement_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.get(url)

        self.assertEqual(request.status_code, 200)

    def test_supplement_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        client_vendors = Vendor.get_user_viewable_objects(self.user)
        vendor_id = client_vendors[0].id

        # kind of janky, but create a list of valid IDs that could be passed
        # when serializing
        ingr_comps = IngredientComposition.get_user_viewable_objects(self.user)
        ingr_comps_ids = list(ingr_comps.values_list('id', flat=True))
        ingr_comps_ids = [str(x) for x in ingr_comps_ids]
        ingr_comps_ids = ','.join(ingr_comps_ids)

        request_parameters = {
            'name': 'Glutamine',
            'vendor_id': vendor_id,
            'ingredient_compositions_ids': ingr_comps_ids
        }
        data = json.dumps(request_parameters)

        request = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 201)


class VendorV1Tests(BaseAPIv1Tests):
    TEST_MODEL = Vendor

    def test_vendor_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request_parameters = {
            'name': 'Advil',
            'email': 'advil@advil.com',
            'url:': 'advil.com',
        }
        data = json.dumps(request_parameters)
        request = self.client.post(url, data=data, content_type='application/json')

        self.assertEqual(request.status_code, 201)

    def test_vendor_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.get(url)

        self.assertEqual(request.status_code, 200)
        vendor_names = [item['name'] for item in request.data]

        # we made a default vendor, so that should definitely be in here
        self.assertTrue(DEFAULT_VENDOR_NAME in vendor_names)


class IngredientV1Tests(BaseAPIv1Tests):
    TEST_MODEL = Ingredient

    def test_ingredient_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)

    def test_ingredient_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)

        request_parameters = {
            'name': 'Advil',
            'half_life_minutes': 30,
        }

        data = json.dumps(request_parameters)
        request = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 201)


class IngredientCompositionV1Tests(BaseAPIv1Tests):
    TEST_MODEL = IngredientComposition

    def test_ingredient_composition_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.get(url)

        self.assertEqual(request.status_code, 200)

    def test_ingredient_composition_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)

        request_parameters = {
            'ingredient_id': '1',
            'measurement_id': '1',
            'quantity': 5,
        }
        data = json.dumps(request_parameters)
        request = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 201)
