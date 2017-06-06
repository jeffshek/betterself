import datetime
import factory

from events.models import SupplementEvent
from supplements.models import Supplement


class DemoSupplementFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Supplement
        # this makes any user/names that are passed correctly
        # used as defaults (factory boy is kind of amazing)
        django_get_or_create = ('user', 'name')


class DemoSupplementEventFactory(factory.django.DjangoModelFactory):
    supplement = factory.SubFactory(DemoSupplementFactory,
                                    user=factory.SelfAttribute('..user'),
                                    name=factory.SelfAttribute('..name'))
    quantity = 1
    source = 'web'
    time = datetime.datetime.now()

    class Meta:
        model = SupplementEvent
        exclude = ('name',)
