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
                if 'time' == key[-4:]:
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


class GetRequestsTestsMixinV2(GenericRESTMethodMixin):
    def _get_results_from_response(self, response):
        # pagination puts data into results
        if self.PAGINATION:
            request_data = response.data['results']
        else:
            request_data = response.data

        return request_data

    def test_get_request(self):
        response = self.client_1.get(self.url)
        data = self._get_results_from_response(response)

        self.assertTrue(len(data) > 0)
        self.assertEqual(response.status_code, 200)

    def _get_response_length_from_get(self, client):
        # have to generate a new api-client, since hard to know which user
        response = client.get(self.url)

        self.assertEqual(response.status_code, 200)
        results = self._get_results_from_response(response)
        return len(results)

    def test_get_request_no_data(self):
        # delete all user_1 data
        self.TEST_MODEL.objects.filter(user=self.user_1).delete()

        response = self.client_1.get(self.url)
        data = self._get_results_from_response(response)

        self.assertEqual(len(data), 0)
        self.assertEqual(response.status_code, 200)

    def test_get_contains_expected_keys(self):
        response = self.client_1.get(self.url)
        data = self._get_results_from_response(response)

        first_data_point = data[0]
        serialized_keys = set(first_data_point.keys())
        required_keys = set(self.required_response_keys)

        missing_keys = required_keys - serialized_keys

        self.assertEqual(len(missing_keys), 0)

    def test_get_request_count(self):
        # do a simple check to make sure no user be able to see another users data
        user_1_count = self.TEST_MODEL.objects.filter(user=self.user_1).count()
        user_2_count = self.TEST_MODEL.objects.filter(user=self.user_2).count()

        user_1_request = self.client_1.get(self.url)
        user_2_request = self.client_2.get(self.url)

        if self.PAGINATION:
            request_1_data = user_1_request.data['results']
            request_2_data = user_2_request.data['results']
        else:
            request_1_data = user_1_request.data
            request_2_data = user_2_request.data

        self.assertEqual(len(request_1_data), user_1_count)
        self.assertEqual(len(request_2_data), user_2_count)

    def test_valid_get_request_with_params_filters_correctly(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)

        # make a request w/out a filter, so it should have all the fixtures for user_1
        no_filter_response = self.client_1.get(url)
        results = self._get_results_from_response(no_filter_response)

        for filterable_key in self.filterable_keys:
            # so if the filter was UUID - show all the values for UUID
            # or something like quantity, show all the values for quantity
            filter_values = [result[filterable_key] for result in results]
            filter_values_unique = set(filter_values)

            for value in filter_values_unique:
                request_parameters = {filterable_key: value}
                filtered_response = self.client_1.get(url, request_parameters)
                filtered_results = self._get_results_from_response(filtered_response)

                self.assertEqual(len(filtered_results), filter_values.count(value))

                unique_values_in_filtered_results = {item[filterable_key] for item in filtered_results}
                # if we've filtered on a specific value ... the only unique filtered value should be one
                self.assertEqual(len(unique_values_in_filtered_results), 1)
