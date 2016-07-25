from supplements.fixtures.factories import IngredientFactory


class SupplementModelsFixturesMixin(object):
    # have a simple test class for fixtures
    # and no surprises from factory_boy with changes
    ingredients = []

    @classmethod
    def create_basic_fixtures_from_factory(cls):
        ingredient = IngredientFactory()
        cls.ingredients.append(ingredient)
