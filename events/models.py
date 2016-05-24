from django.db import models

from betterself.mixins import BaseModelWithUserGeneratedContent
from supplements.models import SupplementProduct


class SupplementProductEventComposition(BaseModelWithUserGeneratedContent):
    """
    Unless you put a proxy over this, this should be the meat of all Events tracking ...
    """
    INPUT_SOURCE_CHOICES = (
        ('api', ''),
        ('ios', ''),
        ('android', ''),
        ('web', ''),
    )
    supplement_product = models.ForeignKey(SupplementProduct)
    # seems kind of weird, but if someone drinks 1/2 of a 5 hour energy ...
    quantity = models.FloatField(default=1)
    # source =
