import json
import logging

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from betterself.users.fixtures.factories import UserFactory
from betterself.users.tests.mixins.test_mixins import UsersTestsFixturesMixin

User = get_user_model()

logger = logging.Logger(__name__)


# python manage.py test apis.betterself.v1.tests.test_base


# I'm such an idiot, refactor all of this to be good mixins
# switch them to a template design Pattern ... that way you don't
# have to inherit over and over like a fool
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


# because the base-api-v1 was written a while ago, and you are embarrassed at your stupidity
class BaseAPIv2Tests(TestCase):
    PAGINATION = False

    @classmethod
    def setUpTestData(cls):
        cls.url = API_V1_LIST_CREATE_URL.format(cls.TEST_MODEL.RESOURCE_NAME)
        cls.create_user_fixtures()
        super().setUpTestData()

    @classmethod
    def create_user_fixtures(cls):
        cls.user_1 = UserFactory(username=cls.username_1)
        cls.user_2 = UserFactory(username=cls.username_2)

    @classmethod
    def create_authenticated_user_on_client(cls, client, user):
        client.force_login(user)

        # just a quick check just in case
        assert user.is_authenticated()

        return client

    def setUp(self):
        # this is kind of goofy when we've already set it as a class-attribute, but since there's a high
        # probability someone may change something in the class - run this each time per test
        self.user_1 = User.objects.get(username=self.username_1)
        self.user_2 = User.objects.get(username=self.username_2)

        # user has to be authenticated per each test!
        self.client_1 = self.create_authenticated_user_on_client(APIClient(), self.user_1)
        self.client_2 = self.create_authenticated_user_on_client(APIClient(), self.user_2)

        super().setUp()


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

    def _get_results_from_response(self, response):
        # pagination puts data into results
        if self.PAGINATION:
            request_data = response.data['results']
        else:
            request_data = response.data

        return request_data
