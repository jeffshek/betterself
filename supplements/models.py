from django.db import models
from django.contrib.auth.models import User

from betterself.mixins import BaseModel, BaseModelWithUserGeneratedContent
from vendors.models import Vendor


class Ingredient(BaseModelWithUserGeneratedContent):
    # if some ingredient is longer than 300 characters, prob shouldn't take it.
    name = models.CharField(max_length=300)
    # this is going to be a hard thing to source / scrap, but you do care about this, leave blank
    # but don't let default be zero.
    half_life_minutes = models.PositiveIntegerField(null=True, blank=True)


class MeasurementUnit(BaseModel):
    name = models.CharField(max_length=100)  # 'milligram'
    short_name = models.CharField(max_length=100, null=True, blank=True)  # 'ml'
    is_liquid = models.BooleanField(default=False)


class IngredientComposition(BaseModelWithUserGeneratedContent):
    """
    Creatine, 5, grams
    """
    ingredient = models.ForeignKey(Ingredient)
    measurement_unit = models.ForeignKey(MeasurementUnit)
    quantity = models.FloatField(default=1)


class SupplementProduct(BaseModelWithUserGeneratedContent):
    """
    Could be a stack like BCAA (which would have 4 ingredient comps)
    Or could just be something simple like Caffeine.
    """
    ingredient_composition = models.ManyToManyField(IngredientComposition)
    vendor = models.ForeignKey(Vendor, null=True)


# TD - All unique constraints to all of these
