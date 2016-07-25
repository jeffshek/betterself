from supplements.fixtures.factories import IngredientFactory, MeasurementFactory, IngredientCompositionFactory


class SupplementModelsFixturesMixin(object):
    # have a simple test class for fixtures
    # and no surprises from factory_boy with changes
    ingredients = []
    measurements = []
    ingredient_compositions = []

    @classmethod
    def create_basic_fixtures_from_factories(cls):
        ingredient = IngredientFactory()
        cls.ingredients.append(ingredient)

        measurement = MeasurementFactory()
        cls.measurements.append(measurement)

        ingredient_composition = IngredientCompositionFactory()
        cls.ingredient_compositions.append(ingredient_composition)

        # supplement = SupplementFactory.create(ingredient_composition=(ingredient_composition,))
