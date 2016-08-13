import json

from apis.betterself.v1.tests import BaseAPIv1Tests
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from supplements.models import Supplement, IngredientComposition, Ingredient, Measurement
from vendors.fixtures.factories import DEFAULT_VENDOR_NAME
from vendors.models import Vendor


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

        contains_ids = [item['id'] for item in request.data]
        # cannot use assertNone
        self.assertTrue(len(contains_ids) > 0)

        self.assertEqual(request.status_code, 200)
        vendor_names = [item['name'] for item in request.data]

        # we made a default vendor, so that should definitely be in here
        self.assertTrue(DEFAULT_VENDOR_NAME in vendor_names)


class MeasurementV1Tests(BaseAPIv1Tests):
    # measurements should ONLY read-only
    TEST_MODEL = Measurement

    def test_measurement_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.get(url)

        self.assertTrue(len(request.data) > 1)
        self.assertEqual(request.status_code, 200)

    def test_measurement_get_request_with_name(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request_parameters = {
            'name': 'milligram',
        }
        # don't do application/json for single key/value, issue with unpacking
        request = self.client.get(url, request_parameters)
        self.assertIsNotNone(request.data)
        self.assertEqual(request.status_code, 200)

    def test_measurement_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.put(url)

        self.assertEqual(request.status_code, 405)


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
