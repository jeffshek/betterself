import datetime
import factory

from events.models import SupplementEvent
from supplements.models import Supplement


class DemoSupplementFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Supplement


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
