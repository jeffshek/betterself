import json

from apis.betterself.v1.tests import BaseAPIv1Tests
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement, IngredientComposition, Ingredient, Measurement
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
    def test_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.get(url)

        self.assertTrue(len(request.data) > 0)
        self.assertEqual(request.status_code, 200)

    def test_valid_get_request_with_params(self, request_parameters):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)

        # don't do application/json for single key/value, issue with unpacking
        request = self.client.get(url, request_parameters)
        self.assertIsNotNone(request.data)
        self.assertTrue(len(request.data) > 0)
        self.assertEqual(request.status_code, 200)

    def test_valid_get_request_for_key_in_response(self, request_parameters, key_check):
        """ Do a get request, and then check for a certain key type"""
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.get(url)

        contains_ids = [item['id'] for item in request.data]
        key_check_items = [item[key_check] for item in request.data]

        # cannot use assertNone
        self.assertTrue(len(contains_ids) > 0)
        self.assertEqual(request.status_code, 200)
        self.assertTrue(len(key_check_items) > 0)


class PostRequestsTestsMixin(GenericRESTVerbsMixin):
    def test_post_request(self, parameters=None):
        post_parameters = parameters if parameters else self.DEFAULT_POST_PARAMS

        # multiple users should be able to create the same object
        request = self._make_post_request(self.client, post_parameters)
        self.assertEqual(request.status_code, 201)

        second_request = self._make_post_request(self.client_2, post_parameters)
        self.assertEqual(second_request.status_code, 201)

        # multiple attempts should still be fine ... although i feel like 201 really be 200
        third_request = self._make_post_request(self.client_2, post_parameters)
        self.assertEqual(third_request.status_code, 201)

        # now let's make sure that different users should be accessing different objects
        client_1_objects_count = self.TEST_MODEL.objects.filter(user=self.user).count()
        client_2_objects_count = self.TEST_MODEL.objects.filter(user=self.user_2).count()

        self.assertTrue(client_1_objects_count > 0)
        self.assertTrue(client_2_objects_count > 0)

    def test_post_request_increments(self, parameters=None):
        """
        Count how many objects are in a model, put a new object in there
        and see how many return back
        """
        # hard to dynamically set default post parameters for objects with heavy relationships
        post_parameters = parameters if parameters else self.DEFAULT_POST_PARAMS
        request = self._make_get_request(self.client)
        data_items_count = len(request.data)

        self._make_post_request(self.client, post_parameters)
        second_request = self._make_get_request(self.client)
        updated_data_items_count = len(second_request.data)

        # since you did only one post, should go up by one
        self.assertEqual(data_items_count + 1, updated_data_items_count)

    def test_post_request_changes_objects_for_right_user(self, parameters=None):
        post_parameters = parameters if parameters else self.DEFAULT_POST_PARAMS

        client_1_starting_request = self._make_get_request(self.client)
        client_1_starting_data_items_count = len(client_1_starting_request.data)
        client_2_starting_request = self._make_get_request(self.client_2)
        client_2_starting_data_items_count = len(client_2_starting_request.data)

        self._make_post_request(self.client_2, post_parameters)

        client_1_second_request = self._make_get_request(self.client)
        client_1_second_data_items_count = len(client_1_second_request.data)
        client_2_second_request = self._make_get_request(self.client_2)
        client_2_second_data_items_count = len(client_2_second_request.data)

        self.assertEqual(client_1_starting_data_items_count, client_1_second_data_items_count)
        self.assertNotEquals(client_2_starting_data_items_count, client_2_second_data_items_count)


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

    def test_valid_get_request_with_params(self):
        request_parameters = {'name': 'milligram'}
        super().test_valid_get_request_with_params(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        request_parameters = {'name': 'milligram'}
        key = 'name'
        super().test_valid_get_request_for_key_in_response(request_parameters, key)

    def test_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client.put(url)

        # expected to fail, this is a read-only set of stuff
        self.assertEqual(request.status_code, 405)


class IngredientV1Tests(SupplementBaseTests, GetRequestsTestsMixin, PostRequestsTestsMixin):
    TEST_MODEL = Ingredient
    DEFAULT_POST_PARAMS = {
        'name': 'Advil',
        'half_life_minutes': 30,
    }

    def test_valid_get_request_with_params(self):
        request_parameters = {'name': 'Advil'}
        super().test_valid_get_request_with_params(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        request_parameters = {'quantity': 5}
        key = 'name'
        super().test_valid_get_request_for_key_in_response(request_parameters, key)


class IngredientCompositionV1Tests(SupplementBaseTests, PostRequestsTestsMixin, GetRequestsTestsMixin):
    TEST_MODEL = IngredientComposition
    DEFAULT_POST_PARAMS = {
        'ingredient_id': '1',
        'measurement_id': '1',
        'quantity': 5,
    }

    def test_valid_get_request_with_params(self):
        request_parameters = {'name': 'Glutamine'}
        super().test_valid_get_request_with_params(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        request_parameters = {'quantity': 5}
        key = 'ingredient'
        super().test_valid_get_request_for_key_in_response(request_parameters, key)


class SupplementV1Tests(SupplementBaseTests, GetRequestsTestsMixin, PostRequestsTestsMixin):
    TEST_MODEL = Supplement

    def _get_default_post_parameters(self):
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
        return request_parameters

    def test_post_request(self):
        request_parameters = self._get_default_post_parameters()
        super().test_post_request(request_parameters)

    def test_post_request_increments(self):
        request_parameters = self._get_default_post_parameters()
        super().test_post_request_increments(request_parameters)

    def test_post_request_changes_objects_for_right_user(self):
        request_parameters = self._get_default_post_parameters()
        super().test_post_request_changes_objects_for_right_user(request_parameters)

    def test_valid_get_request_with_params(self):
        request_parameters = {'name': 'Glutamine'}
        super().test_valid_get_request_with_params(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        request_parameters = {'name': 'Glutamine'}
        key = 'name'
        super().test_valid_get_request_for_key_in_response(request_parameters, key)
