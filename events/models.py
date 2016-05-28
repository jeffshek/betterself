from django.db import models

from betterself.mixins import BaseModelWithUserGeneratedContent
from betterself.utils import create_django_choice_tuple_from_list
from supplements.models import SupplementProduct


class SupplementProductEventComposition(BaseModelWithUserGeneratedContent):
    """
    Unless a proxy goes over this, this should be the meat of all Events tracking ...
    # event tables should be better designed for very large quantity of events
    # since django model id is constrained to 2^31, but if we hit 2^31,
    # will figure that out when we get there ...
    """
    INPUT_SOURCES = [
        'api',
        'ios',
        'android',
        'web',
    ]

    INPUT_SOURCE_CHOICES = create_django_choice_tuple_from_list(INPUT_SOURCES)
    supplement_product = models.ForeignKey(SupplementProduct)
    # floatfield, if ie. someone drinks 1/2 of a 5 hour energy ...
    quantity = models.FloatField(default=1)





