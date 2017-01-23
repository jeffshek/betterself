import json
import logging

from django.test import TestCase
from rest_framework.test import APIClient

from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from betterself.users.tests.mixins.test_mixins import UsersTestsFixturesMixin

logger = logging.Logger(__name__)


# python manage.py test apis.betterself.v1.tests.test_base


# I'm such an idiot, refactor all of this to be good mixins
# switch them to a template design Pattern ... that way you don't
# have to super over and over like a fool
class BaseAPIv1Tests(TestCase, UsersTestsFixturesMixin):
    @classmethod
    def setUpTestData(cls):
        # i don't know how much i like this after seeing this a while later
        # but the base_tests create user fixtures that are logged in for client 1 and client2
        # this becomes useful because there are a lot of fixtures created from the "default"
        cls.create_user_fixtures()
        super(BaseAPIv1Tests, cls).setUpTestData()

    def setUp(self):
        # user has to be authenticated per each test!
        self.client_1 = self.create_authenticated_user_on_client(APIClient(), self.user_1)
        self.client_2 = self.create_authenticated_user_on_client(APIClient(), self.user_2)


class GenericRESTMethodMixin(object):
    def _make_post_request(self, client, request_parameters):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        data = json.dumps(request_parameters)
        request = client.post(url, data=data, content_type='application/json')
        return request

    def _make_get_request(self, client):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = client.get(url)
        return request


class GetRequestsTestsMixin(GenericRESTMethodMixin):
    def test_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)

        self.assertTrue(len(request.data) > 0)
        self.assertEqual(request.status_code, 200)

    def test_valid_get_request_with_params(self, request_parameters):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)

        # don't do application/json for single key/value, issue with unpacking
        request = self.client_1.get(url, request_parameters)

        for record in request.data:
            # if we are using a get with request parameters, we want to be certain
            # that it's correctly filtering on those request_parameters correctly
            # ie. if I filter for anything with a quantity of 5.0, i only get
            # 5.0 back! Build a dictionary containing only what was in the
            # request parameters and compare that it's equal
            record_values = {key: record[key] for key in request_parameters}

            self.assertEqual(record_values, request_parameters)

        self.assertIsNotNone(request.data)
        self.assertTrue(len(request.data) > 0)
        self.assertEqual(request.status_code, 200)

    def test_valid_get_request_for_key_in_response(self, request_parameters, key_check):
        """ Do a get request, and then check for a certain key type"""
        # TD - Refactor so key_check is a list of keys ...
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)

        contains_ids = [item['uuid'] for item in request.data]
        key_check_items = [item[key_check] for item in request.data]

        # cannot use assertNone
        self.assertTrue(len(contains_ids) > 0)
        self.assertEqual(request.status_code, 200)
        self.assertTrue(len(key_check_items) > 0)

    def test_valid_get_on_uuid(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)

        # if this isn't true, we'll blindly say this test is passing
        # when once the amount of objects is greater than 1 in real use cases
        # it'll be returning the wrong objects instantly
        self.assertTrue(len(request.data) > 1)

        request_first_data_point = request.data[0]
        first_data_point_uuid = request_first_data_point['uuid']

        # now make another request, but specifically pick a uuid
        # it should only return an object with that uuid
        parameters = {'uuid': first_data_point_uuid}
        second_request = self.client_1.get(url, parameters)
        result = second_request.data[0]
        result_uuid = result['uuid']

        self.assertEqual(first_data_point_uuid, result_uuid)
        # if we filter by uuid, it's unique there should only be one!
        self.assertEqual(len(second_request.data), 1)


class PostRequestsTestsMixin(GenericRESTMethodMixin):
    def test_post_request(self, parameters=None):
        post_parameters = parameters if parameters else self.DEFAULT_POST_PARAMS

        # multiple users should be able to create the same object
        request = self._make_post_request(self.client_1, post_parameters)
        self.assertEqual(request.status_code, 201)

        second_request = self._make_post_request(self.client_2, post_parameters)
        self.assertEqual(second_request.status_code, 201)

        # multiple attempts should still be fine ... although i feel like 201 really be 200
        third_request = self._make_post_request(self.client_2, post_parameters)
        self.assertEqual(third_request.status_code, 201)

        # now let's make sure that different users should be accessing different objects
        client_1_objects_count = self.TEST_MODEL.objects.filter(user=self.user_1).count()
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
        request = self._make_get_request(self.client_1)
        data_items_count = len(request.data)

        self._make_post_request(self.client_1, post_parameters)
        second_request = self._make_get_request(self.client_1)
        updated_data_items_count = len(second_request.data)

        # since you did only one post, should go up by one
        self.assertEqual(data_items_count + 1, updated_data_items_count)

    def test_post_request_changes_objects_for_right_user(self, parameters=None):
        post_parameters = parameters if parameters else self.DEFAULT_POST_PARAMS

        client_1_starting_get_request = self._make_get_request(self.client_1)
        client_1_starting_data_items_count = len(client_1_starting_get_request.data)
        client_2_starting_get_request = self._make_get_request(self.client_2)
        client_2_starting_data_items_count = len(client_2_starting_get_request.data)

        self._make_post_request(self.client_2, post_parameters)

        client_1_second_get_request = self._make_get_request(self.client_1)
        client_1_second_data_items_count = len(client_1_second_get_request.data)
        client_2_second_request = self._make_get_request(self.client_2)
        client_2_second_data_items_count = len(client_2_second_request.data)

        self.assertEqual(client_1_starting_data_items_count, client_1_second_data_items_count)
        self.assertNotEquals(client_2_starting_data_items_count, client_2_second_data_items_count)

    def test_empty_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.post(url)
        self.assertEqual(request.status_code, 400)
