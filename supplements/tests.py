from django.test import TestCase

from supplements.fixtures.factories import DEFAULT_INGREDIENT_NAME, DEFAULT_INGREDIENT_HL_MINUTE
from supplements.fixtures.mixins import SupplementModelsFixturesGenerator
from supplements.models import Ingredient


class SupplementFixtureCreationTests(TestCase, SupplementModelsFixturesGenerator):
    @classmethod
    def setUpTestData(cls):
        SupplementModelsFixturesGenerator.create_basic_fixtures_from_factories()

    def test_ingredients_creation(self):
        ingredient = Ingredient.objects.all().first()
        self.assertTrue(ingredient)

    def test_default_ingredient(self):
        default_ingredient = Ingredient.objects.all().first()

        self.assertEqual(default_ingredient.name, DEFAULT_INGREDIENT_NAME)
        self.assertEqual(default_ingredient.half_life_minutes, DEFAULT_INGREDIENT_HL_MINUTE)

    def test_default_ingredient_saved(self):
        # realized this happened when factory_boy wasn't saving
        # because it doesn't natively call django create
        saved_ingredients = Ingredient.objects.all().count()
        self.assertTrue(saved_ingredients > 0)
