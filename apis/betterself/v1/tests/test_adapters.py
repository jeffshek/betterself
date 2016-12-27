from django.test import LiveServerTestCase

from apis.betterself.v1.adapters import BetterSelfAPIAdapter
from apis.betterself.v1.constants import VALID_REST_RESOURCES
from betterself.users.models import User
from vendors.fixtures.factories import VendorFactory
from vendors.models import Vendor

"""
This inherits LiveServerTestCase since we're spin up a port to listen and test
adapters responds correctly. Most of the tests here are functional and not integration
tests
"""


class TestAdapters(LiveServerTestCase):
    """
    python manage.py test apis.betterself.v1.tests.test_adapters
    """
    @classmethod
    def setUpClass(cls):
        default_user, _ = User.objects.get_or_create(username='default')
        VendorFactory(user=default_user, name='MadScienceLabs')
        super().setUpClass()

    def setUp(self):
        self.default_user, _ = User.objects.get_or_create(username='default')
        self.adapter = BetterSelfAPIAdapter(self.default_user)
        super().setUp()

    def test_resources_get_on_adapter(self):
        for resource in VALID_REST_RESOURCES:
            response = self.adapter.get_resource_response(resource)
        self.assertEqual(response.status_code, 200)

    def test_get_vendor_view_handles_filters(self):
        parameters = {
            'name': 'FakeFakeVendor',
        }
        data = self.adapter.get_resource(Vendor, parameters=parameters)
        self.assertEqual(len(data), 0)
