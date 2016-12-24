from django.contrib.auth import get_user_model

from supplements.fixtures.factories import IngredientFactory, MeasurementFactory, IngredientCompositionFactory, \
    SupplementFactory, DEFAULT_INGREDIENT_DETAILS_1, DEFAULT_MEASUREMENT_DETAILS, DEFAULT_INGREDIENT_DETAILS_2, \
    DEFAULT_INGREDIENT_DETAILS_3


class SupplementModelsFixturesGenerator(object):
    @classmethod
    def create_fixtures(cls):
        User = get_user_model()
        default_user, _ = User.objects.get_or_create(username='default')

        # use a create on certain factories to allow many to many relationships
        # a bit of debate since there are a lot of defaults in the factory ...
        # not sure how much I like that since that's not overly explicit
        measurement = MeasurementFactory(**DEFAULT_MEASUREMENT_DETAILS)

        ingredient_1 = IngredientFactory(user=default_user, **DEFAULT_INGREDIENT_DETAILS_1)
        ingredient_2 = IngredientFactory(user=default_user, **DEFAULT_INGREDIENT_DETAILS_2)
        ingredient_3 = IngredientFactory(user=default_user, **DEFAULT_INGREDIENT_DETAILS_3)

        # kind of a gotcha, but IngredientCompositionFactory will auto populate
        # foreign keys if the factory specifies it
        ingredient_composition_1 = IngredientCompositionFactory(
            user=default_user, ingredient=ingredient_1, measurement=measurement
        )

        ingredient_composition_2 = IngredientCompositionFactory(
            user=default_user, ingredient=ingredient_2, measurement=measurement
        )
        ingredient_composition_3 = IngredientCompositionFactory(
            user=default_user, ingredient=ingredient_3, measurement=measurement
        )

        # factory boy is a little bit special for many to many
        SupplementFactory.create(user=default_user, ingredient_composition=(
            ingredient_composition_1, ingredient_composition_2, ingredient_composition_3))
