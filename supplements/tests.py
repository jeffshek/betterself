from django.test import TestCase

from supplements.fixtures.factories import DEFAULT_INGREDIENT_NAME_1, DEFAULT_INGREDIENT_HL_MINUTE_1
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Ingredient


class SupplementFixtureCreationTests(TestCase, SupplementModelsFixturesGenerator):
    @classmethod
    def setUpTestData(cls):
        SupplementModelsFixturesGenerator.create_fixtures()

    def test_ingredients_creation(self):
        ingredient = Ingredient.objects.all().first()
        self.assertTrue(ingredient)

    def test_default_ingredient(self):
        default_ingredient = Ingredient.objects.all().first()

        self.assertEqual(default_ingredient.name, DEFAULT_INGREDIENT_NAME_1)
        self.assertEqual(default_ingredient.half_life_minutes, DEFAULT_INGREDIENT_HL_MINUTE_1)

    def test_default_ingredient_saved(self):
        # realized this happened when factory_boy wasn't saving
        # because it doesn't natively call django create
        saved_ingredients = Ingredient.objects.all().count()
        self.assertTrue(saved_ingredients > 0)


# TODO - add me back after migrations
# class SupplementEvents(TestCase):
#     def test_cannot_create_obj_without_user(self):
#         with self.assertRaises(IntegrityError):
#             Supplement.objects.create(name='pop')
