# making a bet that factory_boy will pan out as we get more data
import factory

from supplements.models import Ingredient, Measurement, IngredientComposition, Supplement

DEFAULT_INGREDIENT_NAME = 'Leucine'
DEFAULT_INGREDIENT_HL_MINUTE = 50

DEFAULT_MEASUREMENT_NAME = 'milligram'
DEFAULT_MEASUREMENT_SHORT_NAME = 'mg'

DEFAULT_SUPPLEMENT_NAME = 'BCAA'


class IngredientFactory(factory.Factory):
    class Meta:
        model = Ingredient

    name = DEFAULT_INGREDIENT_NAME
    half_life_minutes = DEFAULT_INGREDIENT_HL_MINUTE


class MeasurementFactory(factory.Factory):
    class Meta:
        model = Measurement

    name = DEFAULT_MEASUREMENT_NAME


class IngredientCompositionFactory(factory.Factory):
    class Meta:
        model = IngredientComposition

    ingredient = factory.SubFactory(IngredientFactory)
    measurement_unit = factory.SubFactory(MeasurementFactory)


class SupplementFactory(factory.Factory):
    class Meta:
        model = Supplement

    name = DEFAULT_SUPPLEMENT_NAME

    @factory.post_generation
    def ingredient_composition(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                print (group)
                self.ingredient_composition.add(group)
