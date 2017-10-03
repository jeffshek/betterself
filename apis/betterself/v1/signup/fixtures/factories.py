import datetime
import factory
import pytz

from faker import Faker

from events.models import SupplementEvent, UserActivity, UserActivityEvent, SupplementReminder
from supplements.models import Supplement

fake = Faker()


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


class DemoActivityType(factory.django.DjangoModelFactory):
    class Meta:
        model = UserActivity
        # this makes any user/names that are passed correctly
        # used as defaults (factory boy is kind of amazing)
        django_get_or_create = ('user', 'name')


class DemoActivityEventFactory(factory.django.DjangoModelFactory):
    user_activity = factory.SubFactory(DemoActivityType,
                                       user=factory.SelfAttribute('..user'),
                                       name=factory.SelfAttribute('..name'))

    class Meta:
        model = UserActivityEvent
        exclude = ('name',)


class SupplementReminderFactory(factory.django.DjangoModelFactory):
    reminder_time = fake.date_time_ad()
    quantity = 1
    last_sent_reminder_time = fake.date_time_this_century(tzinfo=pytz.UTC)

    class Meta:
        model = SupplementReminder
