from django.db import models

from betterself.mixins import BaseModel


class Ingredient(BaseModel):
    # if some ingredient is longer than 300 characters, prob shouldn't take it.
    name = models.CharField(max_length=300)
    user_generated = models.BooleanField(default=False)
    half_life_minutes = models.PositiveIntegerField(null=True, blank=True)


class MeasurementUnit(BaseModel):
    name = models.CharField(max_length=100)  # 'milligram'
    short_name = models.CharField(max_length=100)  # 'ml'
    is_liquid = models.BooleanField(default=False)


class IngredientComposition(BaseModel):
    """
    Creatine, 5, grams
    """
    ingredient = models.ManyToManyField(Ingredient)
    measurement_unit = models.ForeignKey(MeasurementUnit)
    quantity = models.FloatField(default=1)


class SupplementProduct(BaseModel):
    """
    Could be a stack like BCAA (which would have 4 ingredient comps)
    Or could just be something simple like Caffeine.
    """
    ingredient_composition = models.ForeignKey(IngredientComposition)
    user_generated = models.BooleanField(default=False)
    # company = models.ForeignKey()
    # is this the best place to denote user derived products?
    # user = models.ForeignKey()
