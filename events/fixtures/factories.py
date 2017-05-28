import factory
from django.utils import timezone

from events.models import SupplementEvent, DailyProductivityLog, UserActivity, UserActivityEvent
from supplements.fixtures.factories import SupplementFactory


class SupplementEventFactory(factory.DjangoModelFactory):
    source = 'api'
    supplement = factory.SubFactory(SupplementFactory)
    quantity = 1
    time = timezone.now()

    class Meta:
        model = SupplementEvent


class DailyProductivityLogFactory(factory.DjangoModelFactory):
    source = 'api'

    very_productive_time_minutes = 10
    productive_time_minutes = 20
    neutral_time_minutes = 30
    distracting_time_minutes = 40
    very_distracting_time_minutes = 50

    class Meta:
        model = DailyProductivityLog


class UserActivityFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = UserActivity


class UserActivityEventFactory(factory.DjangoModelFactory):
    time = timezone.now()
    # way to get the passed user to this factory and pass it down to UserActivityFactory
    activity = factory.SubFactory(UserActivityFactory, user=factory.SelfAttribute('..user'))
    duration_minutes = 0

    class Meta:
        model = UserActivityEvent
