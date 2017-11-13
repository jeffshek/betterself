import factory
from django.utils import timezone
from factory.fuzzy import FuzzyInteger

from events.models import SupplementLog, DailyProductivityLog, UserActivity, UserActivityLog, UserMoodLog


class SupplementEventFactory(factory.DjangoModelFactory):
    source = 'api'
    quantity = 1
    time = timezone.now()

    class Meta:
        model = SupplementLog


class DailyProductivityLogFactory(factory.DjangoModelFactory):
    source = 'api'

    very_productive_time_minutes = FuzzyInteger(10, 30)
    productive_time_minutes = FuzzyInteger(10, 30)
    neutral_time_minutes = FuzzyInteger(10, 30)
    distracting_time_minutes = FuzzyInteger(10, 30)
    very_distracting_time_minutes = FuzzyInteger(10, 30)

    class Meta:
        model = DailyProductivityLog


class UserActivityFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = UserActivity


class UserActivityEventFactory(factory.DjangoModelFactory):
    time = timezone.now()
    # way to get the passed user to this factory and pass it down to UserActivityFactory
    user_activity = factory.SubFactory(UserActivityFactory, user=factory.SelfAttribute('..user'))
    duration_minutes = 0

    class Meta:
        model = UserActivityLog


class UserMoodLogFactory(factory.DjangoModelFactory):
    time = timezone.now()
    value = FuzzyInteger(1, 10)

    class Meta:
        model = UserMoodLog
