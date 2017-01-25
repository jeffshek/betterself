from django.db import models

from betterself.base_models import BaseModelWithUserGeneratedContent
from betterself.utils import create_django_choice_tuple_from_list
from supplements.models import Supplement

INPUT_SOURCES = [
    'api',
    'ios',
    'android',
    'web',
    'user_excel'
]

INPUT_SOURCES_TUPLES = create_django_choice_tuple_from_list(INPUT_SOURCES)


class SupplementEvent(BaseModelWithUserGeneratedContent):
    """
    Unless a proxy goes over this, this should be the meat of all Events tracking ...
    # event tables should be better designed for very large quantity of events
    # since django model id is constrained to 2^31, but if we hit 2^31,
    # will figure that out when we get there ...
    """
    RESOURCE_NAME = 'supplement_events'

    source = models.CharField(max_length=50, choices=INPUT_SOURCES_TUPLES)
    supplement = models.ForeignKey(Supplement)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    # what time did the user take the five hour energy? use the time model
    # so eventually (maybe never) can do half-life analysis
    time = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'time', 'supplement')
        ordering = ['user', '-time']
        verbose_name = 'Supplement Event'
        verbose_name_plural = 'Supplement Events'

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        formatted_time = self.time.strftime('%Y-%m-%d %I:%M%p')
        formatted_quantity = '{:.0f}'.format(self.quantity)

        return '{quantity} {obj.supplement} ' \
               '{time} from {obj.source} event'.format(obj=self, time=formatted_time, quantity=formatted_quantity)


class SleepEventLog(BaseModelWithUserGeneratedContent):
    """
    Represents how many hours of sleep you got COMING into the day.
    If a user slept 5 hours on Sunday night, Monday's log would say 5*60=300

    Mimicking how vendors report it ... since productivity is often driven
    by how many hours of sleep you got the night before.
    """
    source = models.CharField(max_length=50, choices=INPUT_SOURCES_TUPLES)
    sleep_time_minutes = models.IntegerField()  # always should be stored in minutes
    # Odd debate, but what day does this event accurately represent?
    # "I'm tired, I only got 5 hours of sleep." Those 5 hours represent the state of the day
    day = models.DateField()

    class Meta:
        unique_together = (('day', 'user'),)


class DailyProductivityLog(BaseModelWithUserGeneratedContent):
    """
    Represents the daily over-view of how productive a user was on that day, mimics
    RescueTime's concept of productive time, mildly productive, etc.
    """
    source = models.CharField(max_length=50, choices=INPUT_SOURCES_TUPLES)
    day = models.DateField()

    very_productive_time_minutes = models.PositiveIntegerField()
    productive_time_minutes = models.PositiveIntegerField()
    neutral_time_minutes = models.PositiveIntegerField()
    distracting_time_minutes = models.PositiveIntegerField()
    very_distracting_time_minutes = models.PositiveIntegerField()

    class Meta:
        unique_together = (('day', 'user'),)
