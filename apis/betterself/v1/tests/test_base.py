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
    # pagination means does the serializer return results
    # paginated or not, if paginated, the results display slightly different
    PAGINATION = False

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
