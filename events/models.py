from django.core.exceptions import ValidationError
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
    # how long it took to consume
    duration_minutes = models.IntegerField(default=0)

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


# TODO - rename from SleepActivityLog to SleepActivity
class SleepActivityLog(BaseModelWithUserGeneratedContent):
    """
    Records per each time a person falls asleep that combined across 24 hours is a way to see how much sleep
    a person gets.
    """
    RESOURCE_NAME = 'sleep_activities'

    source = models.CharField(max_length=50, choices=INPUT_SOURCES_TUPLES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name = 'Sleep Activity Log'
        verbose_name_plural = 'Sleep Activity Logs'
        ordering = ['user', '-end_time']

    def __str__(self):
        return '{obj.user} {obj.start_time} {obj.end_time}'.format(obj=self)

    def save(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValidationError('End Time must be greater than Start Time')

        # make sure that there are no overlaps for activities
        # https://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
        queryset = SleepActivityLog.objects.filter(user=self.user, end_time__gte=self.start_time,
                                                   start_time__lte=self.end_time)

        # sometimes save just happens for an update, exclude so wont always fail
        if self.pk:
            queryset = queryset.exclude(id=self.pk)

        if queryset.exists():
            raise ValidationError('Overlapping Periods found when saving Sleep Activity. Found {}'.format(queryset))

        super().save(*args, **kwargs)


class UserActivity(BaseModelWithUserGeneratedContent):
    """
    Users will probably put stuff like "Ate Breakfast", but ideally I want something that can
    support an Activity like "Morning Routine" would consists of multiple ActivityActions

    This is why it's set as foreign key from ActivityEvent, I don't want to overengineer and build
    the entire foreign key relationships, but I also don't want to build a crappy hole that I have to dig out of.
    """
    RESOURCE_NAME = 'user_activities'

    name = models.CharField(max_length=300)
    # Was this significant? IE. Got married? Had a Kid? (Congrats!) Had surgery? New Job? Decided to quit smoking?
    # Mark significant events that might change all future events.
    # Eventually used in charts as "markers/signals" in a chart to show
    # IE. Once you decided to quit smoking --- > This is your heart rate.
    is_significant_activity = models.BooleanField(default=False)
    # Is this an user_activity you hate / want to avoid?
    # Are there certain patterns (sleep, diet, supplements, other activities) that lead to negative activities?
    # IE - Limited sleep impact decision making (probably).
    # Can we figure out if there are certain things you do ahead that limit sleep?
    # Can we figure out if there are certain behaviors you can avoid so this doesn't happen?
    # Are there certain foods that will likely cause a negative user_activity?
    # Personally - Eating foods with lots of preservatives causes depression/flu like symptoms that last for 1-2 days
    is_negative_activity = models.BooleanField(default=False)

    class Meta:
        unique_together = (('name', 'user'),)
        ordering = ['name']


class UserActivityEvent(BaseModelWithUserGeneratedContent):
    """
    Represents any particular type of event a user may have done
        - ie. Meditation, running, take dog the park, etc.

    This doesn't really get to the crux of how do you record a state of mind that's
    frustrating like depression/flu (both of which share oddly similar mental states),
    which if this is one thing BetterSelf cures for you, then it's a success.

    I just haven't figured the most appropriate way to model / store such information.
    """
    RESOURCE_NAME = 'user_activity_events'

    user_activity = models.ForeignKey(UserActivity)
    source = models.CharField(max_length=50, choices=INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE)
    duration_minutes = models.IntegerField(default=0)
    time = models.DateTimeField()

    class Meta:
        unique_together = (('time', 'user', 'user_activity'),)
        ordering = ['user', '-time']
