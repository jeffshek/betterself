from uuid import uuid4

from apis.betterself.v1.tests.test_base import GenericRESTMethodMixin
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL


class PUTRequestsTestsMixin(GenericRESTMethodMixin):
    def _get_initial_data(self, data=None):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        if data:
            request = self.client_1.get(url, data=data)
        else:
            request = self.client_1.get(url)

        if self.PAGINATION:
            data = request.data['results']
        else:
            data = request.data

        return data

    def test_put_empty_data_returns_404(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        result = self.client_1.put(url)

        self.assertEqual(result.status_code, 404)

    def test_put_request(self):
        data = self._get_initial_data()

        # take the first object and update something within it
        initial_result = data[0]
        uuid = initial_result.pop('uuid')

        # make a copied result to update with new parameters
        copied_result = initial_result.copy()

        # for any results, if its a string, update them to a constant
        attributes_to_update = [key for key, value in initial_result.items() if isinstance(value, str)]

        STRING_UPDATE_PARAM = 'TEST_POST'
        for attribute in attributes_to_update:
            copied_result[attribute] = STRING_UPDATE_PARAM

        # now add uuid back since that's the one value that should be immutable
        copied_result['uuid'] = uuid

        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        result = self.client_1.put(url, data=copied_result, format='json')

        for attribute in attributes_to_update:
            self.assertTrue(result.data[attribute], STRING_UPDATE_PARAM)

        # now for safe measure, let's use a get to retrieve the same object via UUID
        get_response = self._get_initial_data(data={'uuid': uuid})
        second_result = get_response[0]

        for attribute in attributes_to_update:
            self.assertTrue(second_result[attribute], STRING_UPDATE_PARAM)

    def test_put_request_with_invalid_uuid_will_fail(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        uuid = uuid4()
        crap_response = self.client_1.put(url, {'uuid': uuid})
        self.assertEqual(crap_response.status_code, 404)
