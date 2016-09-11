from django.db import models

from betterself.base_models import BaseModel, BaseModelWithUserGeneratedContent
from vendors.models import Vendor


class Measurement(BaseModel):
    RESOURCE_NAME = 'measurements'

    name = models.CharField(max_length=100)  # 'milligram'
    short_name = models.CharField(max_length=100, null=True, blank=True)  # 'ml'
    is_liquid = models.BooleanField(default=False)

    def __str__(self):
        return '{obj.name}'.format(obj=self)

####
# Not a flat structure because of need to support complex stacks.
####
# 5 Grams of BCAA (Branched Chained Amino Acid). BCAA is the Supplement Product
#   Each gram of BCAA has 1.25 of each amino acid.
#       So IngredientComposition is Leucine with 1.25 grams.
#       Ingredient is Leucine.


class Ingredient(BaseModelWithUserGeneratedContent):
    RESOURCE_NAME = 'ingredients'

    # if some ingredient is longer than 300 characters, prob shouldn't take it.
    # if anyone ever reads up reading this, 1,3 dimethylamylamine is probably a great
    # example of if you can't pronounce it, don't take it.
    name = models.CharField(max_length=300)
    # this is going to be a hard thing to source / scrap, but you do care about this, leave blank
    # but don't let default be zero.
    half_life_minutes = models.PositiveIntegerField(null=True, blank=True)


class IngredientComposition(BaseModelWithUserGeneratedContent):
    """ Creatine, 5, grams """
    RESOURCE_NAME = 'ingredient_compositions'

    ingredient = models.ForeignKey(Ingredient)
    measurement = models.ForeignKey(Measurement, null=True, blank=True)
    quantity = models.FloatField(default=1)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.measurement:
            return '{ingredient.name} ({obj.quantity} {measurement.name})'.format(obj=self, ingredient=self.ingredient,
                measurement=self.measurement)
        elif self.quantity != 1:
            return '{ingredient.name} ({obj.quantity})'.format(obj=self, ingredient=self.ingredient)
        else:
            return '{ingredient.name}'.format(ingredient=self.ingredient)


class Supplement(BaseModelWithUserGeneratedContent):
    """
    Could be a stack like BCAA (which would have 4 ingredient comps)
    Or could just be something simple like Caffeine.
    """
    RESOURCE_NAME = 'supplements'

    name = models.CharField(max_length=300)
    ingredient_compositions = models.ManyToManyField(IngredientComposition, blank=True)
    vendor = models.ForeignKey(Vendor, null=True, blank=True)
    # quantity is an event type of attribute, so its not here.

# TD - Add unique constraints to all of these, make sure user is added to unique!
