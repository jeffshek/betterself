import dateutil

from apis.betterself.v1.tests.test_base import GenericRESTMethodMixin
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL


class GetRequestsTestsMixin(GenericRESTMethodMixin):
    def test_get_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)

        self.assertTrue(len(request.data) > 0)
        self.assertEqual(request.status_code, 200)

    def test_valid_get_request_with_params_filters_correctly(self, request_parameters):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)

        # don't do application/json for single key/value, issue with unpacking
        request = self.client_1.get(url, request_parameters)

        # pagination views puts data in "results"
        if self.PAGINATION:
            request_data = request.data['results']
        else:
            request_data = request.data

        for record in request_data:
            # if we are using a get with request parameters, we want to be certain
            # that it's correctly filtering on those request_parameters correctly
            # ie. if I filter for anything with a quantity of 5.0, i only get
            # 5.0 back! Build a dictionary containing only what was in the
            # request parameters and compare that it's equal
            record_values = {key: record[key] for key in request_parameters}

            # a bit of a hack, but string responses of datetimes can change slightly
            # based on how zero utc is represented, here bring the object back to datetime
            # and then isoformat it out again
            for key in record_values:
                if 'time' in key:
                    returned_time_string = record_values[key]
                    serialized_time_string = dateutil.parser.parse(returned_time_string).isoformat()

                    record_values[key] = serialized_time_string

            self.assertEqual(record_values, request_parameters)

        self.assertIsNotNone(request_data)
        self.assertTrue(len(request_data) > 0)
        self.assertEqual(request.status_code, 200)

    def test_valid_get_request_for_key_in_response(self, key_check):
        """ Do a get request, and then check for a certain key type"""
        # TD - Refactor so key_check is a list of keys ...
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)

        # pagination views puts data in "results
        if self.PAGINATION:
            request_data = request.data['results']
        else:
            request_data = request.data

        contains_ids = [item['uuid'] for item in request_data]
        key_check_items = [item[key_check] for item in request_data]

        # cannot use assertNone
        self.assertTrue(len(contains_ids) > 0)
        self.assertEqual(request.status_code, 200)
        self.assertTrue(len(key_check_items) > 0)

    def test_valid_get_on_uuid(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.get(url)

        # pagination views puts data in "results"
        if self.PAGINATION:
            request_data = request.data['results']
        else:
            request_data = request.data

        # this assumes that the fixtures data will create more than 1 record!
        self.assertTrue(len(request_data) > 1)

        # if this isn't true, we'll blindly say this test is passing
        # when once the amount of objects is greater than 1 in real use cases
        # it'll be returning the wrong objects instantly
        request_first_data_point = request_data[0]
        first_data_point_uuid = request_first_data_point['uuid']

        # now make another request, but specifically pick a uuid
        # it should only return an object with that uuid
        parameters = {'uuid': first_data_point_uuid}
        second_request = self.client_1.get(url, parameters)

        # pagination views puts data in "results
        if self.PAGINATION:
            second_request_data = second_request.data['results']
        else:
            second_request_data = second_request.data

        result = second_request_data[0]
        result_uuid = result['uuid']

        self.assertEqual(first_data_point_uuid, result_uuid)
        # if we filter by uuid, it's unique there should only be one!
        self.assertEqual(len(second_request_data), 1)
