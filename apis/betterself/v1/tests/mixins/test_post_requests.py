from apis.betterself.v1.tests.test_base import GenericRESTMethodMixin
from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL


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

        # pagination views puts data in "results
        if self.PAGINATION:
            data_items_count = request.data['count']
        else:
            request_data = request.data
            data_items_count = len(request_data)

        self._make_post_request(self.client_1, post_parameters)
        second_request = self._make_get_request(self.client_1)

        # pagination views puts data in "results
        if self.PAGINATION:
            updated_data_items_count = second_request.data['count']
        else:
            second_request_data = second_request.data
            updated_data_items_count = len(second_request_data)

        # since you did only one post, should go up by one
        self.assertEqual(data_items_count + 1, updated_data_items_count)

    def test_post_request_changes_objects_for_right_user(self, parameters=None):
        post_parameters = parameters if parameters else self.DEFAULT_POST_PARAMS

        client_1_starting_get_request = self._make_get_request(self.client_1)
        client_2_starting_get_request = self._make_get_request(self.client_2)

        self._make_post_request(self.client_2, post_parameters)

        client_1_second_get_request = self._make_get_request(self.client_1)
        client_2_second_get_request = self._make_get_request(self.client_2)

        if self.PAGINATION:
            client_1_starting_data_items_count = client_1_starting_get_request.data['count']
            client_1_second_data_items_count = client_1_second_get_request.data['count']

            client_2_starting_data_items_count = client_2_starting_get_request.data['count']
            client_2_second_data_items_count = client_2_second_get_request.data['count']
        else:
            client_1_starting_data_items_count = len(client_1_starting_get_request.data)
            client_1_second_data_items_count = len(client_1_second_get_request.data)

            client_2_starting_data_items_count = len(client_2_starting_get_request.data)
            client_2_second_data_items_count = len(client_2_second_get_request.data)

        self.assertEqual(client_1_starting_data_items_count, client_1_second_data_items_count)
        self.assertNotEquals(client_2_starting_data_items_count, client_2_second_data_items_count)

    def test_empty_post_request(self):
        url = API_V1_LIST_CREATE_URL.format(self.TEST_MODEL.RESOURCE_NAME)
        request = self.client_1.post(url)
        self.assertEqual(request.status_code, 400)
