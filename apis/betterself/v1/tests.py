import logging

from django.test import TestCase
from rest_framework.test import APIClient

from apis.betterself.v1.urls import API_V1_LIST_CREATE_URL
from betterself.users.tests.mixins.test_mixins import UsersTestsMixin
from supplements.models import Supplement

VALID_GET_RESOURCES = [
    Supplement.RESOURCE_NAME,
]

logger = logging.Logger(__name__)
logger.setLevel(logging.ERROR)


SECONDARY_CREDENTIALS = {
    'username': 'tester2',
    'email': 'username@gmail.com',  # i hate that django allows multiple emails to be created
    'password': 'secret_password',
}


class BaseAPIv1Tests(TestCase, UsersTestsMixin):
    @classmethod
    def setUpTestData(cls):
        # setup the user once
        cls.user = cls.create_user()
        # create some random fake user_2 to test duplicates
        cls.user_2 = cls.create_user(SECONDARY_CREDENTIALS)
        super(BaseAPIv1Tests, cls).setUpTestData()

    def setUp(self):
        # user has to be authenticated per each test!
        self.client = self.create_authenticated_user_on_client(APIClient(), self.user)
        self.client_2 = self.create_authenticated_user_on_client(APIClient(), self.user_2)

    @staticmethod
    def debug_request(request):
        """ Helper function that outputs everything for easier reading """
        logger.error('\n***Debugging Request***')
        logger.error(request.data)
        logger.error(request.status_code)


class GeneralAPIv1Tests(BaseAPIv1Tests):
    def test_fake_resources_404(self):
        url = API_V1_LIST_CREATE_URL.format('fake_made_up_resource')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 404)

    def test_all_resources_have_valid_get(self):
        for resource in VALID_GET_RESOURCES:
            url = API_V1_LIST_CREATE_URL.format(resource)
            request = self.client.get(url)
            self.assertEqual(request.status_code, 200)
