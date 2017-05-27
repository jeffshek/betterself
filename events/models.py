from django.db import models

from betterself.base_models import BaseModelWithUserGeneratedContent
from betterself.utils import create_django_choice_tuple_from_list
from supplements.models import Supplement

WEB_INPUT_SOURCE = 'web'

INPUT_SOURCES = [
    'api',
    'ios',
    'android',
    WEB_INPUT_SOURCE,
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
    # how long in minutes was the supplement consumed
    # TODO - change this to duration_minutes to match everything else
    duration = models.IntegerField(default=0)

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


class DailyProductivityLog(BaseModelWithUserGeneratedContent):
    """
    Represents the daily over-view of how productive a user was on that day, mimics
    RescueTime's concept of productive time, mildly productive, etc.
    """
    RESOURCE_NAME = 'productivity_log'

    source = models.CharField(max_length=50, choices=INPUT_SOURCES_TUPLES)
    date = models.DateField()

    very_productive_time_minutes = models.PositiveIntegerField(null=True, blank=True)
    productive_time_minutes = models.PositiveIntegerField(null=True, blank=True)
    neutral_time_minutes = models.PositiveIntegerField(null=True, blank=True)
    distracting_time_minutes = models.PositiveIntegerField(null=True, blank=True)
    very_distracting_time_minutes = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Daily Productivity Log'
        verbose_name_plural = 'Daily Productivity Logs'
        unique_together = (('date', 'user'),)
        ordering = ['-date']


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
    date = models.DateField()

    class Meta:
        unique_together = (('date', 'user'),)


class ActivityEvent(BaseModelWithUserGeneratedContent):
    """
    Represents any particular type of event a user may have done
        - ie. Meditation, running, take dog the park, etc.

    This doesn't really get to the crux of how do you record a state of mind that's
    frustrating like depression/flu (both of which share oddly similar mental states),
    which if this is one thing BetterSelf cures for you, then it's a success.

    I just haven't figured the most appropriate way to model / store such information.
    """
    source = models.CharField(max_length=50, choices=INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE)
    duration_minutes = models.IntegerField(default=0)
    # Was this significant? IE. You got married? Kid? Had surgery? New Job? Decided to quit smoking?
    # Record all significant events that might change all future decisions.
    # You want to model it so this can be done as markers/signals in a "how this is how you've changed chart"
    is_significant_event = models.BooleanField(default=False)
    # Was this an activity you hate / want to avoid?
    # Recording negative events as X happened, why?
    # Are there certain patterns (sleep, diet, supplements, other activities) that lead to negative activities?
    # IE - It's been shown that limited sleep seems to impact decision making. Let's try to chart/model that.
    # I'm also quite convinced personally certain food leads to really bad feelings of depression/flu-like symptoms in
    # <12 hours.
    is_negative_event = models.BooleanField(default=False)
