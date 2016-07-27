from supplements.fixtures.factories import IngredientFactory, MeasurementFactory, IngredientCompositionFactory, \
    SupplementFactory, DEFAULT_INGREDIENT_DETAILS, DEFAULT_MEASUREMENT_DETAILS


class SupplementModelsFixturesGenerator(object):
    @classmethod
    def create_factory_fixtures(cls):
        # use a create on certain factories to allow many to many relationships
        # a bit of debate since there are a lot of defaults in the factory ...
        # not sure how much I like that since that's not overly explicit
        measurement = MeasurementFactory(**DEFAULT_MEASUREMENT_DETAILS)

        ingredient = IngredientFactory(**DEFAULT_INGREDIENT_DETAILS)

        # kind of a gotcha, but IngredientCompositionFactory will auto populate
        # foreign keys if the factory specifies it
        ingredient_composition = IngredientCompositionFactory(
            ingredient=ingredient, measurement_unit=measurement
        )

        # factory boy is a little bit special for many to many
        SupplementFactory.create(ingredient_composition=(ingredient_composition,))
