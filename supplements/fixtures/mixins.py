from supplements.fixtures.factories import IngredientFactory, MeasurementFactory, IngredientCompositionFactory, \
    SupplementFactory


class SupplementModelsFixturesGenerator(object):
    @classmethod
    def create_basic_fixtures_from_factories(cls):
        # use a create on certain factories to allow many to many relationships
        IngredientFactory()
        MeasurementFactory()
        ingredient_composition = IngredientCompositionFactory()
        SupplementFactory.create(ingredient_composition=(ingredient_composition,))
