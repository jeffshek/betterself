from apis.betterself.v1.tests.test_base import BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from supplements.fixtures.factories import DEFAULT_INGREDIENT_NAME_1
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement, IngredientComposition, Ingredient, Measurement
from vendors.fixtures.factories import DEFAULT_VENDOR_NAME
from vendors.fixtures.mixins import VendorModelsFixturesGenerator
from vendors.models import Vendor


#  python manage.py test apis.betterself.v1.supplements.tests

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


class VendorV1Tests(SupplementBaseTests, PostRequestsTestsMixin, GetRequestsTestsMixin):
    TEST_MODEL = Vendor
    DEFAULT_POST_PARAMS = {
        'name': 'Poptarts',
        'email': 'general_hosptial@school.com',
        'url:': 'cool.com',
    }

    def test_valid_get_request_with_params(self):
        request_parameters = {'name': DEFAULT_VENDOR_NAME}
        super().test_valid_get_request_with_params(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        key = 'name'
        super().test_valid_get_request_for_key_in_response(key)


class MeasurementV1Tests(SupplementBaseTests, GetRequestsTestsMixin):
    # measurements should be ONLY read-only
    TEST_MODEL = Measurement

    def test_valid_get_request_with_params(self):
        request_parameters = {'name': 'milligram'}
        super().test_valid_get_request_with_params(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        key = 'name'
        super().test_valid_get_request_for_key_in_response(key)

    def test_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.put(url)

        # expected to fail, this is a read-only set of stuff
        self.assertEqual(request.status_code, 405)


class IngredientV1Tests(SupplementBaseTests, GetRequestsTestsMixin, PostRequestsTestsMixin):
    TEST_MODEL = Ingredient
    DEFAULT_POST_PARAMS = {
        'name': 'Advil',
        'half_life_minutes': 30,
    }

    def test_valid_get_request_with_params(self):
        request_parameters = {'name': DEFAULT_INGREDIENT_NAME_1}
        super().test_valid_get_request_with_params(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        key = 'name'
        super().test_valid_get_request_for_key_in_response(key)


class IngredientCompositionV1Tests(SupplementBaseTests, PostRequestsTestsMixin, GetRequestsTestsMixin):
    TEST_MODEL = IngredientComposition
    DEFAULT_POST_PARAMS = {
        'quantity': 5,
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.DEFAULT_POST_PARAMS['ingredient_uuid'] = Ingredient.objects.all().first().uuid.__str__()
        cls.DEFAULT_POST_PARAMS['measurement_uuid'] = Measurement.objects.all().first().uuid.__str__()

    def test_valid_get_request_with_params(self):
        request_parameters = {'quantity': 1}
        super().test_valid_get_request_with_params(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        key = 'ingredient'
        super().test_valid_get_request_for_key_in_response(key)

    def test_valid_get_with_ingredient_uuid(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        # get the first valid data point
        result = self.client_1.get(url).data[0]
        result_ingredient_uuid = result['ingredient']['uuid']

        parameters = {'ingredient_uuid': result_ingredient_uuid}
        data = self.client_1.get(url, parameters).data
        ingredient_uuids_found = [item['ingredient']['uuid'] for item in data]
        ingredient_uuids_found = set(ingredient_uuids_found)

        self.assertEqual(len(ingredient_uuids_found), 1)
        self.assertEqual(result_ingredient_uuid, ingredient_uuids_found.pop())

    def test_valid_get_with_measurement_uuid(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        # get the first valid data point
        result = self.client_1.get(url).data[0]
        result_measurement_uuid = result['measurement']['uuid']

        parameters = {'measurement_uuid': result_measurement_uuid}
        data = self.client_1.get(url, parameters).data
        measurement_uuids_found = [item['measurement']['uuid'] for item in data]
        measurement_uuids_found = set(measurement_uuids_found)

        self.assertEqual(len(measurement_uuids_found), 1)
        self.assertEqual(result_measurement_uuid, measurement_uuids_found.pop())


class SupplementV1Tests(SupplementBaseTests, GetRequestsTestsMixin, PostRequestsTestsMixin):
    # python manage.py test apis.betterself.v1.supplements.tests.SupplementV1Tests
    TEST_MODEL = Supplement

    def _get_default_post_parameters(self):
        client_vendors = Vendor.get_user_viewable_objects(self.user_1)
        vendor_id = client_vendors[0].uuid.__str__()

        # kind of whack, but create a list of valid IDs that could be passed
        # when serializing
        ingr_comps = IngredientComposition.get_user_viewable_objects(self.user_1)
        ingr_comps_uuids = ingr_comps.values_list('uuid', flat=True)
        ingr_comps_uuids = [{'uuid': str(item)} for item in ingr_comps_uuids]

        request_parameters = {
            'name': 'Glutamine',
            'vendor_uuid': vendor_id,
            'ingredient_compositions': ingr_comps_uuids
        }
        return request_parameters

    def test_default_parameters_recorded_correctly(self):
        request_parameters = self._get_default_post_parameters()

        self._make_post_request(self.client_1, request_parameters)

        supplement = Supplement.objects.get(name=request_parameters['name'])
        vendor_uuid = str(supplement.vendor.uuid)

        ingr_comps_uuids = supplement.ingredient_compositions.values_list('uuid', flat=True)
        ingr_comps_uuids = set(str(uuid) for uuid in ingr_comps_uuids)

        request_ingredient_compositions = request_parameters['ingredient_compositions']
        request_ingredient_compositions_uuids = set(item['uuid'] for item in request_ingredient_compositions)

        self.assertEqual(vendor_uuid, request_parameters['vendor_uuid'])
        self.assertSetEqual(request_ingredient_compositions_uuids, ingr_comps_uuids)

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
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)
        data = request.data
        first_name = data[0]['name']

        request_parameters = {'name': first_name}
        super().test_valid_get_request_with_params(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        key = 'name'
        super().test_valid_get_request_for_key_in_response(key)
