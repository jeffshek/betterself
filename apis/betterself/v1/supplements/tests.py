from apis.betterself.v1.tests.test_base import BaseAPIv1Tests, GetRequestsTestsMixin, PostRequestsTestsMixin
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from supplements.fixtures.factories import DEFAULT_INGREDIENT_NAME_1, DEFAULT_INGREDIENT_HL_MINUTE_1
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


class VendorV1Tests(SupplementBaseTests, PostRequestsTestsMixin):
    TEST_MODEL = Vendor
    DEFAULT_POST_PARAMS = {
        'name': 'Poptarts',
        'email': 'general_hosptial@school.com',
        'url:': 'cool.com',
    }


class MeasurementV1Tests(SupplementBaseTests, GetRequestsTestsMixin):
    # measurements should be ONLY read-only
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
        request_parameters = {'half_life_minutes': DEFAULT_INGREDIENT_HL_MINUTE_1}
        key = 'name'
        super().test_valid_get_request_for_key_in_response(request_parameters, key)


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
        request_parameters = {'name': 'Glutamine'}
        super().test_valid_get_request_with_params(request_parameters)

    def test_valid_get_request_for_key_in_response(self):
        request_parameters = {'quantity': 5}
        key = 'ingredient'
        super().test_valid_get_request_for_key_in_response(request_parameters, key)


class SupplementV1Tests(SupplementBaseTests, GetRequestsTestsMixin, PostRequestsTestsMixin):
    TEST_MODEL = Supplement

    def _get_default_post_parameters(self):
        client_vendors = Vendor.get_user_viewable_objects(self.user_1)
        vendor_id = client_vendors[0].id

        # kind of whack, but create a list of valid IDs that could be passed
        # when serializing
        ingr_comps = IngredientComposition.get_user_viewable_objects(self.user_1)
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
