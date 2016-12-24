from django.contrib.auth import get_user_model

from vendors.fixtures.factories import VendorFactory, DEFAULT_VENDOR_NAME


class VendorModelsFixturesGenerator(object):
    @classmethod
    def create_fixtures(cls):
        User = get_user_model()
        default_user, _ = User.objects.get_or_create(username='default')

        VendorFactory(user=default_user, name=DEFAULT_VENDOR_NAME)
        VendorFactory(user=default_user, name='MadScienceLabs')
