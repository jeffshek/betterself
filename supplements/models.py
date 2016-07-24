from django.db import models

from vendors.models import Vendor
from betterself.base_models import BaseModel, BaseModelWithUserGeneratedContent


####
# Why this is not a FLAT structure. Need to support complex stacks.
####
# 5 Grams of BCAA (Branched Chained Amino Acid). BCAA is the Supplement Product
#   Each gram of BCAA has 1.25 of each amino acid.
#       So IngredientComposition is Leucine with 1.25 grams.
#       Ingredient is Leucine.


# ingredient is such a weird word to spell
class Ingredient(BaseModelWithUserGeneratedContent):
    # if some ingredient is longer than 300 characters, prob shouldn't take it.
    # if anyone ever reads up reading this, 1,3 dimethylamylamine is probably a great
    # example of if you can't pronounce it, don't take it.
    name = models.CharField(max_length=300)
    # this is going to be a hard thing to source / scrap, but you do care about this, leave blank
    # but don't let default be zero.
    half_life_minutes = models.PositiveIntegerField(null=True, blank=True)


class Measurement(BaseModel):
    name = models.CharField(max_length=100)  # 'milligram'
    short_name = models.CharField(max_length=100, null=True, blank=True)  # 'ml'
    is_liquid = models.BooleanField(default=False)


class IngredientComposition(BaseModelWithUserGeneratedContent):
    """
    Creatine, 5, grams
    """
    ingredient = models.ForeignKey(Ingredient)
    measurement_unit = models.ForeignKey(Measurement, null=True)
    quantity = models.FloatField(default=1)


class Supplement(BaseModelWithUserGeneratedContent):
    """
    Could be a stack like BCAA (which would have 4 ingredient comps)
    Or could just be something simple like Caffeine.
    """
    name = models.CharField(max_length=300)
    ingredient_composition = models.ManyToManyField(IngredientComposition)
    vendor = models.ForeignKey(Vendor, null=True)
    # quantity is an event type of attribute, so its not here.

# TD - Add unique constraints to all of these, make sure user is added to unique!
