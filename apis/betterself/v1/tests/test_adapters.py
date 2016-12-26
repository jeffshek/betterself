from django.test import LiveServerTestCase

from apis.betterself.v1.adapters import BetterSelfAPIAdapter
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from betterself.users.models import User
from betterself.users.tests.mixins.test_mixins import UsersTestsFixturesMixin
from vendors.models import Vendor

"""
This inherits LiveServerTestCase since we're spin up a port to listen and test
adapters responds correctly. Most of the tests here are functional and not integration
tests
"""


class TestAdapters(LiveServerTestCase, UsersTestsFixturesMixin):
    """
    python manage.py test apis.betterself.v1.tests.test_adapters
    """
    @classmethod
    def setUpTestData(cls):
        cls._create_user_fixtures()
        super(BaseAPIv1Tests, cls).setUpTestData()

    def setUp(self):
        super().setUp()

    def test_resources_get_on_adapter(self):
        default_user, _ = User.objects.get_or_create(username='default')
        adapter = BetterSelfAPIAdapter(default_user)
        response = adapter.get_resource(Vendor)
        self.assertEqual(response.status_code, 200)
