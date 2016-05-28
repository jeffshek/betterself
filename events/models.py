from django.db import models

from betterself.mixins import BaseModelWithUserGeneratedContent
from betterself.utils import create_django_choice_tuple_from_list
from supplements.models import SupplementProduct

INPUT_SOURCES = [
    'api',
    'ios',
    'android',
    'web',
    'user_excel'
]


class SupplementProductEventComposition(BaseModelWithUserGeneratedContent):
    """
    Unless a proxy goes over this, this should be the meat of all Events tracking ...
    # event tables should be better designed for very large quantity of events
    # since django model id is constrained to 2^31, but if we hit 2^31,
    # will figure that out when we get there ...
    """
    input_source = create_django_choice_tuple_from_list(INPUT_SOURCES)
    supplement_product = models.ForeignKey(SupplementProduct)
    # floatfield, if ie. someone drinks 1/2 of a 5 hour energy ...
    quantity = models.FloatField(default=1)
    # what time did the user take the five hour energy? use the time model
    # so not pigeon holed and can do half_life analysis.
    time = models.DateTimeField()


class SleepEventLog(BaseModelWithUserGeneratedContent):
    """
    Represents how many hours of sleep you got COMING into the day.
    If a user slept 5 hours on Sunday night, Monday's log would say 5*60=300

    Mimicing how vendors report it ... since productivty is often driven
    by how many hours of sleep you got the night before.
    """
    input_source = create_django_choice_tuple_from_list(INPUT_SOURCES)
    sleep_time_minutes = models.IntegerField()  # always should be stored in minutes
    # Odd debate, but what day does this event accurately represent?
    # "I'm tired, I only got 5 hours of sleep." Those 5 hours represent the state of the day
    day = models.DateField()



