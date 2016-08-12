from django.db import models

from betterself.base_models import BaseModelWithRequiredUser
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


class SupplementEvent(BaseModelWithRequiredUser):
    """
    Unless a proxy goes over this, this should be the meat of all Events tracking ...
    # event tables should be better designed for very large quantity of events
    # since django model id is constrained to 2^31, but if we hit 2^31,
    # will figure that out when we get there ...
    """
    RESOURCE_NAME = 'supplement_events'

    source = models.CharField(max_length=50, choices=INPUT_SOURCES_TUPLES)
    supplement_product = models.ForeignKey(Supplement)
    # floatfield, if ie. someone drinks 1/2 of a 5 hour energy ...
    quantity = models.FloatField(default=1)
    # what time did the user take the five hour energy? use the time model
    # so not pigeon holed and can do half_life analysis.
    time = models.DateTimeField()


class SleepEventLog(BaseModelWithRequiredUser):
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
