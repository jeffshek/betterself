# making a bet that factory_boy will pan out as we get more data
import factory

from supplements.models import Ingredient, Measurement, IngredientComposition, Supplement

DEFAULT_INGREDIENT_NAME_1 = 'Leucine'
DEFAULT_INGREDIENT_HL_MINUTE_1 = 50
DEFAULT_INGREDIENT_DETAILS_1 = {
    'name': DEFAULT_INGREDIENT_NAME_1,
    'half_life_minutes': DEFAULT_INGREDIENT_HL_MINUTE_1
}

DEFAULT_INGREDIENT_NAME_2 = 'Valine'
DEFAULT_INGREDIENT_HL_MINUTE_2 = 50
DEFAULT_INGREDIENT_DETAILS_2 = {
    'name': DEFAULT_INGREDIENT_NAME_2,
    'half_life_minutes': DEFAULT_INGREDIENT_HL_MINUTE_2
}

DEFAULT_INGREDIENT_NAME_3 = 'Isoleucine'
DEFAULT_INGREDIENT_HL_MINUTE_3 = 50
DEFAULT_INGREDIENT_DETAILS_3 = {
    'name': DEFAULT_INGREDIENT_NAME_3,
    'half_life_minutes': DEFAULT_INGREDIENT_HL_MINUTE_3
}

DEFAULT_MEASUREMENT_NAME = 'milligram'
DEFAULT_MEASUREMENT_SHORT_NAME = 'mg'
DEFAULT_MEASUREMENT_DETAILS = {
    'name': DEFAULT_INGREDIENT_NAME_1,
    'short_name': DEFAULT_MEASUREMENT_SHORT_NAME,
}

DEFAULT_SUPPLEMENT_NAME = 'BCAA'


class IngredientFactory(factory.DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = DEFAULT_INGREDIENT_NAME_1
    half_life_minutes = DEFAULT_INGREDIENT_HL_MINUTE_1


class MeasurementFactory(factory.DjangoModelFactory):
    class Meta:
        model = Measurement

    name = DEFAULT_MEASUREMENT_NAME


class IngredientCompositionFactory(factory.DjangoModelFactory):
    class Meta:
        model = IngredientComposition

    ingredient = factory.SubFactory(IngredientFactory)
    measurement = factory.SubFactory(MeasurementFactory)


class SupplementFactory(factory.DjangoModelFactory):
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
                self.ingredient_compositions.add(group)
