import json

from apis.betterself.v1.tests import BaseAPIv1Tests
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement, IngredientComposition, Ingredient, Measurement
from vendors.fixtures.factories import DEFAULT_VENDOR_NAME
from vendors.fixtures.mixins import VendorModelsFixturesGenerator
from vendors.models import Vendor


class SupplementBaseTests(BaseAPIv1Tests):
    # maybe debate this might be better as a template design pattern ...
    # this inheritance chain is getting pretty long
    @classmethod
    def setUpTestData(cls):
        # generic fixtures based on the apps, inclusive of all the models
        # there, so supplement/models includes ingredients, etc.
        SupplementModelsFixturesGenerator.create_fixtures()
        VendorModelsFixturesGenerator.create_fixtures()

        super().setUpTestData()


class GenericRESTVerbsMixin(object):
    def _make_post_request(self, client, request_parameters):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        data = json.dumps(request_parameters)
        request = client.post(url, data=data, content_type='application/json')
        return request

    def _make_get_request(self, client):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = client.get(url)
        return request


class GetRequestsTestsMixin(GenericRESTVerbsMixin):
    def test_measurement_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.get(url)

        self.assertTrue(len(request.data) > 1)
        self.assertEqual(request.status_code, 200)


class PostRequestsTestsMixin(GenericRESTVerbsMixin):
    def test_vendor_post_request(self):
        # multiple users should be able to create the same object
        request = self._make_post_request(self.client, self.DEFAULT_POST_PARAMS)
        self.assertEqual(request.status_code, 201)

        second_request = self._make_post_request(self.client_2, self.DEFAULT_POST_PARAMS)
        self.assertEqual(second_request.status_code, 201)

        # multiple attempts should still be fine ... although i feel like 201 really be 200
        third_request = self._make_post_request(self.client_2, self.DEFAULT_POST_PARAMS)
        self.assertEqual(third_request.status_code, 201)

        # now let's make sure that different users should be accessing different objects
        client_1_models_count = self.TEST_MODEL.objects.filter(user=self.user).count()
        client_2_models_count = self.TEST_MODEL.objects.filter(user=self.user_2).count()

        self.assertTrue(client_1_models_count > 0)
        self.assertTrue(client_2_models_count > 0)

    def test_vendor_post_request_increments(self):
        """
        Count how many objects are in vendor, put a new object in there
        and see how many return back
        """
        request = self._make_get_request(self.client)
        data_items_count = len(request.data)

        self._make_post_request(self.client, self.DEFAULT_POST_PARAMS)
        second_request = self._make_get_request(self.client)
        updated_data_items_count = len(second_request.data)

        # since you did only one post, should go up by one
        self.assertEqual(data_items_count + 1, updated_data_items_count)

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


class VendorV1Tests(SupplementBaseTests, PostRequestsTestsMixin):
    TEST_MODEL = Vendor
    DEFAULT_POST_PARAMS = {
        'name': 'Poptarts',
        'email': 'general_hosptial@school.com',
        'url:': 'cool.com',
    }


class MeasurementV1Tests(SupplementBaseTests, GetRequestsTestsMixin):
    # measurements should ONLY read-only
    TEST_MODEL = Measurement

    def test_measurement_get_request_with_name(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request_parameters = {
            'name': 'milligram',
        }
        # don't do application/json for single key/value, issue with unpacking
        request = self.client.get(url, request_parameters)
        self.assertIsNotNone(request.data)
        self.assertEqual(request.status_code, 200)

    def test__post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.put(url)

        # expected to fail, no one should be able to update this
        self.assertEqual(request.status_code, 405)


class IngredientV1Tests(SupplementBaseTests):
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


class IngredientCompositionV1Tests(SupplementBaseTests):
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


class SupplementV1Tests(SupplementBaseTests):
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
