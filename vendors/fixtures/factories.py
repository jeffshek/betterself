import factory

from vendors.models import Vendor

DEFAULT_VENDOR_NAME = 'Advil'


class VendorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Vendor

    name = DEFAULT_VENDOR_NAME
    email = factory.LazyAttribute(lambda a: 'scientist@{0}.com'.format(a.name))
    url = factory.LazyAttribute(lambda a: '{0}.com'.format(a.name))
