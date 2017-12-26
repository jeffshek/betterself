from apis.betterself.v1.tests.mixins.test_get_requests import GetRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_post_requests import PostRequestsTestsMixin
from apis.betterself.v1.tests.mixins.test_put_requests import PUTRequestsTestsMixin
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from events.fixtures.mixins import UserSupplementStackFixturesGenerator
from supplements.fixtures.factories import DEFAULT_INGREDIENT_NAME_1, UserSupplementStackFactory, SupplementFactory
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Supplement, IngredientComposition, Ingredient, Measurement, UserSupplementStack, \
    UserSupplementStackComposition
from vendors.fixtures.factories import DEFAULT_VENDOR_NAME
from vendors.fixtures.mixins import VendorModelsFixturesGenerator
from vendors.models import Vendor


#  I heavily dislike what you made here now, the inheritance is toooooo much.

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

    def test_valid_get_request_with_params_filters_correctly(self):
        request_parameters = {'name': DEFAULT_VENDOR_NAME}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        key = 'name'
        super().test_valid_get_request_for_key_in_response(key)


class MeasurementV1Tests(SupplementBaseTests, GetRequestsTestsMixin):
    # measurements should be ONLY read-only
    TEST_MODEL = Measurement

    def test_valid_get_request_with_params_filters_correctly(self):
        request_parameters = {'name': 'milligram'}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)

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

    def test_valid_get_request_with_params_filters_correctly(self):
        request_parameters = {'name': DEFAULT_INGREDIENT_NAME_1}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)

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

    def test_valid_get_request_with_params_filters_correctly(self):
        request_parameters = {'quantity': 1}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)

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


class SupplementV1Tests(SupplementBaseTests, GetRequestsTestsMixin, PostRequestsTestsMixin, PUTRequestsTestsMixin):
    # python manage.py test apis.betterself.v1.supplements.tests.SupplementV1Tests
    TEST_MODEL = Supplement

    def _get_default_post_parameters(self):
        # kind of whack, but create a list of valid IDs that could be passed
        # when serializing
        ingr_comps = IngredientComposition.objects.filter(user=self.user_1)
        ingr_comps_uuids = ingr_comps.values_list('uuid', flat=True)
        ingr_comps_uuids = [{'uuid': str(item)} for item in ingr_comps_uuids]

        request_parameters = {
            'name': 'Glutamine',
            'ingredient_compositions': ingr_comps_uuids
        }
        return request_parameters

    def test_default_parameters_recorded_correctly(self):
        request_parameters = self._get_default_post_parameters()

        self._make_post_request(self.client_1, request_parameters)

        supplement = Supplement.objects.get(name=request_parameters['name'])

        ingr_comps_uuids = supplement.ingredient_compositions.values_list('uuid', flat=True)
        ingr_comps_uuids = set(str(uuid) for uuid in ingr_comps_uuids)

        request_ingredient_compositions = request_parameters['ingredient_compositions']
        request_ingredient_compositions_uuids = set(item['uuid'] for item in request_ingredient_compositions)

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

    def test_valid_get_request_with_params_filters_correctly(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)
        data = request.data
        first_name = data[0]['name']

        request_parameters = {'name': first_name}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        key = 'name'
        super().test_valid_get_request_for_key_in_response(key)

    def test_put_parameter_updates_supplement_name(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)
        supplement_uuid = request.data[0]['uuid']

        modified_supplement_name = 'Cheeseburgers'

        data = {
            'uuid': supplement_uuid,
            'name': modified_supplement_name
        }

        response = self.client_1.put(url, data)
        self.assertEqual(response.data['name'], modified_supplement_name)

        # for good measure, let's send another request (this time via a GET) to make sure that it's updated correctly
        uuid_filter = {'uuid': supplement_uuid}
        response = self.client_1.get(url, uuid_filter)
        self.assertEqual(response.data[0]['name'], modified_supplement_name)

    def test_put_parameter_updates_ingredient_uuids_correctly(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)

        supplement_uuid = request.data[0]['uuid']
        supplement_ingredients = request.data[0]['ingredient_compositions']
        supplement_ingredients_uuids = [item['uuid'] for item in supplement_ingredients]

        # if the fixtures ever get modified / messed up, fixtures need to ensure this is greater than one
        self.assertTrue(len(supplement_ingredients_uuids) > 1)

        supplement_ingredients_uuid_to_use = supplement_ingredients_uuids[0]

        data = {
            'uuid': supplement_uuid,
            'ingredient_compositions': [{'uuid': supplement_ingredients_uuid_to_use}]
        }

        response = self.client_1.put(url, data, format='json')

        self.assertEqual(response.data['uuid'], supplement_uuid)
        self.assertEqual(response.data['ingredient_compositions'][0]['uuid'], supplement_ingredients_uuid_to_use)

    def test_put_parameter_when_ingredient_uuid_is_wrong(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)

        supplement_uuid = request.data[0]['uuid']
        supplement_ingredients = request.data[0]['ingredient_compositions']
        supplement_ingredients_uuids = [item['uuid'] for item in supplement_ingredients]

        # if the fixtures ever get modified / messed up, fixtures need to ensure this is greater than one
        self.assertTrue(len(supplement_ingredients_uuids) > 1)

        supplement_ingredients_uuid_to_use = supplement_ingredients_uuids[0]

        data = {
            'uuid': supplement_uuid,
            # ingredient_compositions should be sent as a list of dictionaries, here we send it as a dictionary
            'ingredient_compositions': {'uuid': supplement_ingredients_uuid_to_use}
        }

        response = self.client_1.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_request_work_uuid_filter_works_for_filtering_on_compositions(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)

        supplement_ingredients = request.data[0]['ingredient_compositions']
        supplement_ingredients_uuids = [item['uuid'] for item in supplement_ingredients]
        supplement_ingredients_uuid = supplement_ingredients_uuids[0]

        # filter on a composition to see if it returns back
        uuid_filter_url = '{url}?ingredient_compositions_uuids={supplement_ingredients_uuid}'.format(
            url=url, supplement_ingredients_uuid=supplement_ingredients_uuids[0])

        uuid_request = self.client_1.get(uuid_filter_url)
        self.assertEqual(uuid_request.status_code, 200)

        length_of_compositions = len(uuid_request.data)
        ingredient_composition = IngredientComposition.objects.filter(uuid=supplement_ingredients_uuid)
        supplements_with_same_composition = Supplement.objects.filter(ingredient_compositions=ingredient_composition)

        self.assertEqual(length_of_compositions, supplements_with_same_composition.count())


class SupplementStackV1Tests(SupplementBaseTests, GetRequestsTestsMixin, PostRequestsTestsMixin, PUTRequestsTestsMixin):
    TEST_MODEL = UserSupplementStack

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        UserSupplementStackFixturesGenerator.create_fixtures(cls.user_1)

    def _get_default_post_parameters(self):
        # kind of whack, but create a list of valid IDs that could be passed
        # when serializing
        supplements = Supplement.objects.filter(user=self.user_1)
        supplements_uuids = supplements.values_list('uuid', flat=True)
        supplements_uuids = [{'supplement_uuid': str(item)} for item in supplements_uuids]

        request_parameters = {
            'name': 'Glutamine',
            'compositions': supplements_uuids
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

    def test_valid_get_request_for_key_in_response(self):
        key = 'name'
        super().test_valid_get_request_for_key_in_response(key)

    def test_valid_get_request_with_params_filters_correctly(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)
        data = request.data
        first_name = data[0]['name']

        request_parameters = {'name': first_name}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)


class UserSupplementStackCompositionViewsetTests(SupplementBaseTests, GetRequestsTestsMixin, PostRequestsTestsMixin):
    TEST_MODEL = UserSupplementStackComposition

    def _get_default_post_parameters(self):
        stack = UserSupplementStackFactory(user=self.user_1)
        supplement = SupplementFactory(user=self.user_1)
        request_params = {
            'stack_uuid': str(stack.uuid),
            'supplement_uuid': str(supplement.uuid)
        }
        return request_params

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        UserSupplementStackFixturesGenerator.create_fixtures(cls.user_1)

    def test_valid_get_request_for_key_in_response(self):
        key = 'supplement'
        super().test_valid_get_request_for_key_in_response(key)

    def test_valid_get_request_with_params_filters_correctly(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)
        data = request.data
        uuid = data[0]['uuid']

        request_parameters = {'uuid': uuid}
        super().test_valid_get_request_with_params_filters_correctly(request_parameters)

    def test_post_request(self):
        request_parameters = self._get_default_post_parameters()
        super().test_post_request(request_parameters)

    def test_post_request_increments(self):
        request_parameters = self._get_default_post_parameters()
        super().test_post_request_increments(request_parameters)

    def test_post_request_changes_objects_for_right_user(self):
        request_parameters = self._get_default_post_parameters()
        super().test_post_request_changes_objects_for_right_user(request_parameters)
