from vendors.fixtures.factories import VendorFactory, DEFAULT_VENDOR_NAME


class VendorModelsFixturesGenerator(object):
    @classmethod
    def create_fixtures(cls):
        VendorFactory(name=DEFAULT_VENDOR_NAME)
        VendorFactory(name='MadScienceLabs')
