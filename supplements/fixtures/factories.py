# making a bet that factory_boy will pan out as we get more data
import factory

from supplements.models import Ingredient


class IngredientFactory(factory.Factory):
    class Meta:
        model = Ingredient

    name = 'Leucine'
    half_life_minutes = 50
