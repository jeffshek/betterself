from django.db import models

from betterself.mixins import BaseTimeModel


class Ingredient(BaseTimeModel):
    # if some ingredient is longer than 300 characters, prob shouldn't take it.
    name = models.CharField(max_length=300)
    user_generated = models.BooleanField(default=False)
    half_life_minutes = models.PositiveIntegerField(null=True, blank=True)



