import numbers
from dateutil import parser
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

    def test_put_requests_with_booleans(self):
        data = self._get_initial_data()

        # take the first object and update something within it
        initial_result = data[0]
        uuid = initial_result.pop('uuid')

        # make a copied result to update with new parameters
        copied_result = initial_result.copy()

        # get only numbers params, but make sure that the numbers don't include true/false
        copied_result = {k: v for k, v in copied_result.items()
                         if isinstance(v, bool)}

        # for any results, if its a string, update them to a constant
        attributes_to_update = list(copied_result.keys())

        for bool_update in [True, False]:
            bool_update_parameter = bool_update

            for attribute in attributes_to_update:
                copied_result[attribute] = bool_update_parameter

            # now add uuid back since that's the one value that should be immutable
            copied_result['uuid'] = uuid

            url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
            result = self.client_1.put(url, data=copied_result, format='json')

            for attribute in attributes_to_update:
                self.assertEqual(result.data[attribute], bool_update_parameter)

            # now for safe measure, let's use a get to retrieve the same object via UUID
            get_response = self._get_initial_data(data={'uuid': uuid})
            second_result = get_response[0]

            for attribute in attributes_to_update:
                self.assertEqual(second_result[attribute], bool_update_parameter)

    def test_put_request_with_numbers(self):
        data = self._get_initial_data()

        # take the first object and update something within it
        initial_result = data[0]
        uuid = initial_result.pop('uuid')

        # make a copied result to update with new parameters
        copied_result = initial_result.copy()

        # get only numbers params, but make sure that the numbers don't include true/false
        copied_result = {k: v for k, v in copied_result.items()
                         if isinstance(v, numbers.Real)
                         and not isinstance(v, bool)}

        # for any results, if its a string, update them to a constant
        attributes_to_update = list(copied_result.keys())

        for number_to_try in [5, 10.0]:
            number_update_param = number_to_try

            for attribute in attributes_to_update:
                copied_result[attribute] = number_update_param

            # now add uuid back since that's the one value that should be immutable
            copied_result['uuid'] = uuid

            url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
            result = self.client_1.put(url, data=copied_result, format='json')

            for attribute in attributes_to_update:
                self.assertEqual(result.data[attribute], number_update_param, result.data)

            # now for safe measure, let's use a get to retrieve the same object via UUID
            get_response = self._get_initial_data(data={'uuid': uuid})
            second_result = get_response[0]

            for attribute in attributes_to_update:
                self.assertEqual(second_result[attribute], number_update_param)

    def test_put_request_updates_for_strings(self):
        """
        This test is literally garbage now that I come back and look at this.
        """
        data = self._get_initial_data()

        # take the first object and update something within it
        initial_result = data[0]
        uuid = initial_result.pop('uuid')

        # make a copied result to update with new parameters
        copied_result = initial_result.copy()
        # don't update anything that's a list or a dictionary
        # also include an ignore list where certain attributes are read-only
        readonly_parameters = ['supplement_name', 'supplement_uuid', 'description']
        copied_result = {k: v for k, v in copied_result.items() if isinstance(v, str) and k not in readonly_parameters}

        # for any results, if its a string, update them to a constant "aka" api, since we know that's accepted in
        # tuple validation
        attributes_to_update = list(copied_result.keys())

        string_update_param = 'api'
        for attribute in attributes_to_update:
            try:
                parser.parse(copied_result[attribute])
                # don't update datetime variables
                copied_result.pop(attribute)
                continue
            except ValueError:
                pass

            copied_result[attribute] = string_update_param

        # since we updated a few that no longer should be updated, let's refresh this list
        attributes_to_update = list(copied_result.keys())

        # now add uuid back since that's the one value that should be immutable
        copied_result['uuid'] = uuid

        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        result = self.client_1.put(url, data=copied_result, format='json')

        for attribute in attributes_to_update:
            # we are ignoring all the notes field since that can be dynamically generated
            if attribute == 'notes':
                continue

            self.assertEqual(result.data[attribute], string_update_param)

        # now for safe measure, let's use a get to retrieve the same object via UUID
        get_response = self._get_initial_data(data={'uuid': uuid})
        second_result = get_response[0]

        for attribute in attributes_to_update:
            # we are ignoring all the notes field since that can be dynamically generated
            if attribute == 'notes':
                continue

            self.assertEqual(second_result[attribute], string_update_param)

    def test_put_request_with_invalid_uuid_will_fail(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        uuid = uuid4()
        crap_response = self.client_1.put(url, {'uuid': uuid})
        self.assertEqual(crap_response.status_code, 404)
