# making a bet that factory_boy will pan out as we get more data
import factory

from supplements.models import Ingredient

DEFAULT_INGREDIENT_NAME = 'Leucine'
DEFAULT_INGREDIENT_HL_MINUTE = 50


class IngredientFactory(factory.Factory):
    class Meta:
        model = Ingredient

    name = DEFAULT_INGREDIENT_NAME
    half_life_minutes = DEFAULT_INGREDIENT_HL_MINUTE
