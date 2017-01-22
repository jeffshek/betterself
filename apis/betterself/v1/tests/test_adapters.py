from django.test import LiveServerTestCase, TestCase
from django.utils import timezone

from apis.betterself.v1.adapters import BetterSelfAPIAdapter
from apis.betterself.v1.constants import VALID_REST_RESOURCES
from betterself.users.models import User
from events.fixtures.factories import SupplementEventFactory
from events.models import SupplementEvent
from supplements.fixtures.factories import IngredientFactory, IngredientCompositionFactory, SupplementFactory
from supplements.models import Ingredient, IngredientComposition, Measurement, Supplement
from vendors.fixtures.factories import VendorFactory
from vendors.models import Vendor

MOCK_VENDOR_NAME = 'MadScienceLabs'
MOCK_INGREDIENT_NAME = 'BCAA'


# python manage.py test apis.betterself.v1.tests.test_adapters

class TestResourceMixin(object):
    def test_get_resource(self):
        data = self.adapter.get_resource_data(self.model)
        self.assertTrue(len(data) > 0)

    def test_get_resource_if_none_exist(self):
        self.model.objects.all().delete()

        data = self.adapter.get_resource_data(self.model)
        self.assertTrue(len(data) == 0)

    def test_get_resource_if_none_belong_to_user(self):
        # because all user created objects have limited access to only
        # the user that created it or the default user, check to make sure
        # that any attempts to get data that don't belong ... shouldn't
        records = self.adapter.get_resource_data(self.model)
        records_prior_update = len(records)

        nobody = User.objects.create_user('nobody knows')
        self.model.objects.all().update(user=nobody)

        records = self.adapter.get_resource_data(self.model)
        records_after_update = len(records)

        self.assertEqual(records_after_update, 0)
        self.assertNotEqual(records_prior_update, records_after_update)


"""
This inherits LiveServerTestCase since we're spin up a port to listen and test
adapters responds correctly. Most of the tests here are functional and not pure unit
tests ... there's also some overlap with some of the more basic unit tests
"""


class AdapterTests(LiveServerTestCase, TestCase):
    @classmethod
    def setUpTestData(cls):
        default_user, _ = User.objects.get_or_create(username='default')
        VendorFactory(user=default_user, name=MOCK_VENDOR_NAME)
        ingredient = IngredientFactory(user=default_user, name=MOCK_INGREDIENT_NAME)
        IngredientCompositionFactory(user=default_user, ingredient=ingredient)
        SupplementFactory(user=default_user)

    def setUp(self):
        self.default_user, _ = User.objects.get_or_create(username='default')
        self.adapter = BetterSelfAPIAdapter(self.default_user)
        super().setUp()


class GenericAdapterTests(AdapterTests):
    def test_resources_get_on_adapter(self):
        for resource in VALID_REST_RESOURCES:
            response = self.adapter._get_resource_response(resource)
            self.assertEqual(response.status_code, 200)


class VendorAdapterTests(AdapterTests, TestResourceMixin):
    model = Vendor

    def test_get_vendor_view_handles_empty_filter(self):
        parameters = {
            'name': 'FakeFakeVendor',
        }
        data = self.adapter.get_resource_data(Vendor, parameters=parameters)
        self.assertEqual(len(data), 0)

    def test_get_vendor_view_filters(self):
        parameters = {
            'name': MOCK_VENDOR_NAME,
        }
        data = self.adapter.get_resource_data(Vendor, parameters=parameters)
        self.assertEqual(len(data), 1)

    def test_post_on_vendor_resource(self):
        name = 'non_existent'
        email = 'somefakeemail@gmail.com'

        parameters = {
            'name': name,
            'email': email,
        }

        data = self.adapter.post_resource_data(Vendor, parameters)

        self.assertEqual(data['name'], name)
        self.assertEqual(data['email'], email)


class IngredientAdapterTests(AdapterTests, TestResourceMixin):
    model = Ingredient

    def test_get_ingredient_name_filter(self):
        parameters = {
            'name': MOCK_INGREDIENT_NAME,
        }
        data = self.adapter.get_resource_data(Ingredient, parameters=parameters)
        self.assertEqual(len(data), 1)

    def test_get_ingredient_empty_filter(self):
        parameters = {
            'name': 'non_existent',
        }
        data = self.adapter.get_resource_data(Ingredient, parameters=parameters)
        self.assertEqual(len(data), 0)

    def test_post_ingredient(self):
        mock_name = 'non_existent'
        parameters = {
            'name': mock_name,
        }
        data = self.adapter.post_resource_data(Ingredient, parameters)
        self.assertEqual(data['name'], mock_name)

    def test_post_ingredient_with_half_life_parameters(self):
        mock_name = 'non_existent'
        half_life_minutes = 60
        parameters = {
            'name': mock_name,
            'half_life_minutes': half_life_minutes,
        }
        data = self.adapter.post_resource_data(Ingredient, parameters)

        self.assertEqual(data['name'], mock_name)
        self.assertEqual(data['half_life_minutes'], half_life_minutes)

    def test_post_ingredient_with_numbers_in_half_life(self):
        mock_name = 'non_existent'
        half_life_minutes = '60'
        parameters = {
            'name': mock_name,
            'half_life_minutes': half_life_minutes,
        }
        data = self.adapter.post_resource_data(Ingredient, parameters)

        self.assertEqual(data['name'], mock_name)
        # serializers should automatically take strings and convert to integers
        self.assertEqual(data['half_life_minutes'], int(half_life_minutes))

    def test_post_ingredient_with_nonsensical_uuid(self):
        mock_name = 'non_existent'
        uuid = 'hah'

        parameters = {
            'name': mock_name,
            'uuid': uuid,
        }
        data = self.adapter.post_resource_data(Ingredient, parameters)

        self.assertEqual(data['name'], mock_name)
        # this shouldn't be the same as a new object would be created
        # updates should be done via a put
        self.assertNotEquals(data['uuid'], uuid)


class IngredientCompositionAdapterTests(AdapterTests, TestResourceMixin):
    model = IngredientComposition

    def test_get_filters_on_ingredient_composition(self):
        data = self.adapter.get_resource_data(IngredientComposition)
        for ingredient_composition in data:
            ingredient_uuid = ingredient_composition['ingredient']['uuid']

            # do a lookup based on an ingredient .. make sure we can navigate
            # back and forth based on uuid lookups
            filter_parameters = {
                'ingredient_uuid': ingredient_uuid
            }
            filtered_data = self.adapter.get_resource_data(IngredientComposition, parameters=filter_parameters)
            filtered_data_ingredient_uuids = [result['ingredient']['uuid'] for result in filtered_data]

            self.assertTrue(ingredient_uuid in filtered_data_ingredient_uuids)

    def test_post_ingredient_composition(self):
        # with factories, we know we already created a few of the things to test
        ingredients = self.adapter.get_resource_data(Ingredient)
        ingredient = ingredients[0]
        ingredient_uuid = ingredient['uuid']

        measurements = self.adapter.get_resource_data(Measurement)
        measurement = measurements[0]
        measurement_uuid = measurement['uuid']

        quantity = 10

        parameters = {
            'ingredient_uuid': ingredient_uuid,
            'measurement_uuid': measurement_uuid,
            'quantity': quantity
        }

        data = self.adapter.post_resource_data(IngredientComposition, parameters)

        self.assertEqual(data['measurement_uuid'], measurement['uuid'])
        self.assertEqual(data['ingredient_uuid'], ingredient['uuid'])
        self.assertEqual(data['quantity'], quantity)
        self.assertIsNotNone(data['uuid'])

    def test_post_ingredient_composition_with_invalid_uuid(self):
        ingredients = self.adapter.get_resource_data(Ingredient)
        ingredient = ingredients[0]

        ingredient_uuid = ingredient['uuid']
        measurement_uuid = 'cake_is_lie'
        quantity = 10

        parameters = {
            'ingredient_uuid': ingredient_uuid,
            'measurement_uuid': measurement_uuid,
            'quantity': quantity
        }

        data = self.adapter.post_resource_data(IngredientComposition, parameters)

        # if invalid, no uuid will be passed back, instead all that's sent will be
        # {'measurement_uuid': ['"cake_is_lie" is not a valid UUID.']}
        self.assertIsNone(data.get('uuid'))

    def test_post_ingredient_composition_measurement_isnt_required(self):
        ingredients = self.adapter.get_resource_data(Ingredient)
        ingredient = ingredients[0]
        ingredient_uuid = ingredient['uuid']

        quantity = 10

        parameters = {
            'ingredient_uuid': ingredient_uuid,
            'quantity': quantity
        }

        data = self.adapter.post_resource_data(IngredientComposition, parameters)

        self.assertEqual(data['ingredient_uuid'], ingredient['uuid'])
        self.assertEqual(data['quantity'], quantity)


class SupplementAdapterTests(AdapterTests, TestResourceMixin):
    model = Supplement

    # python manage.py test apis.betterself.v1.tests.test_adapters.SupplementAdapterTests
    def setUp(self):
        self.default_user, _ = User.objects.get_or_create(username='default')
        self.adapter = BetterSelfAPIAdapter(self.default_user)
        super().setUp()

    def test_post_supplements(self):
        supplement_name = 'cheese'
        parameters = {
            'name': supplement_name
        }

        data = self.adapter.post_resource_data(Supplement, parameters=parameters)
        self.assertEqual(data['name'], supplement_name)

    def test_post_supplements_with_invalid_uuid(self):
        supplement_name = 'cheese'
        parameters = {
            'name': supplement_name,
            'ingredient_compositions_uuids': [1, 2],
        }

        data = self.adapter.post_resource_data(Supplement, parameters=parameters)

        # if this errors (ie. something along the lines of
        # {'ingredient_compositions_uuids': ['"2" is not a valid UUID.']}
        self.assertTrue('ingredient_compositions_uuids' in data)
        # when django errors out, it does it by returning the key field with an error
        # and includes nothing else
        self.assertFalse('name' in data)
        self.assertEqual(len(data), 1)

    def test_post_supplements_with_invalid_vendor_uuid(self):
        supplement_name = 'cheese'
        parameters = {
            'name': supplement_name,
            'vendor_uuid': [1, 2],
        }

        data = self.adapter.post_resource_data(Supplement, parameters=parameters)

        # when django errors out, it does it by returning the key field with an error and description
        self.assertTrue('vendor_uuid' in data)
        self.assertEqual(len(data), 1)
        self.assertFalse('name' in data)

    def test_post_supplements_with_non_existent_vendor_uuid(self):
        vendor_uuid = Vendor.objects.all().first().uuid
        supplement_name = 'cheese'
        parameters = {
            'name': supplement_name,
            'vendor_uuid': vendor_uuid,
        }

        # delete all vendor_ids so we can now test out what happens
        Vendor.objects.all().delete()

        data = self.adapter.post_resource_data(Supplement, parameters=parameters)

        # when django errors out, it does it by returning the key field with an error and description
        self.assertTrue('non_field_errors' in data)
        self.assertEqual(len(data), 1)
        self.assertFalse('name' in data)


class SupplementEventsAdaptersTests(AdapterTests, TestResourceMixin):
    model = SupplementEvent

    # python manage.py test apis.betterself.v1.tests.test_adapters.SupplementEventsAdaptersTests
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        default_user, _ = User.objects.get_or_create(username='default')
        SupplementEventFactory(user=default_user)

    def test_post_events(self):
        supplement_uuid = self.adapter.get_resource_data(Supplement)[0]['uuid']
        parameters = {
            'source': 'android',
            'supplement_uuid': supplement_uuid,
            'quantity': 3.5,
            'time': timezone.now()
        }

        data = self.adapter.post_resource_data(SupplementEvent, parameters=parameters)
        self.assertEqual(supplement_uuid, data['supplement_uuid'])

    def test_post_events_with_invalid_uuid(self):
        supplement_uuid = 'woooopeeee'
        parameters = {
            'source': 'android',
            'supplement_uuid': supplement_uuid,
            'quantity': 3.5,
            'time': timezone.now()
        }

        data = self.adapter.post_resource_data(SupplementEvent, parameters=parameters)

        # if error, only the field is returned and an error corresponding
        self.assertTrue('supplement_uuid' in data)
        self.assertEqual(len(data), 1)

    def test_post_events_with_invalid_source(self):
        supplement_uuid = self.adapter.get_resource_data(Supplement)[0]['uuid']
        # this should make source nonsensical
        parameters = {
            'source': supplement_uuid,
            'supplement_uuid': supplement_uuid,
            'quantity': 3.5,
            'time': timezone.now()
        }

        data = self.adapter.post_resource_data(SupplementEvent, parameters=parameters)

        # if error, only the field is returned and an error corresponding
        self.assertTrue('source' in data)
        self.assertEqual(len(data), 1)

    def test_post_events_with_valid_but_no_longer_exists_uuid(self):
        supplement_uuid = self.adapter.get_resource_data(Supplement)[0]['uuid']
        Supplement.objects.all().delete()

        parameters = {
            'source': 'android',
            'supplement_uuid': supplement_uuid,
            'quantity': 3.5,
            'time': timezone.now()
        }

        data = self.adapter.post_resource_data(SupplementEvent, parameters=parameters)

        # if error, only the field is returned and an error corresponding
        self.assertTrue('supplement_uuid' in data)
        self.assertEqual(len(data), 1)

    def test_get_or_create_response(self):
        parameters = {'name': 'Chocolate'}
        ingredient = self.adapter.get_or_create_resource(Ingredient, parameters)
        uuid_first_pass = ingredient['uuid']

        ingredient = self.adapter.get_or_create_resource(Ingredient, parameters)
        uuid_second_pass = ingredient['uuid']

        self.assertEqual(uuid_first_pass, uuid_second_pass)
