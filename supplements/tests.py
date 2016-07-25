from django.test import TestCase

from supplements.fixtures.factories import DEFAULT_INGREDIENT_NAME, DEFAULT_INGREDIENT_HL_MINUTE
from supplements.fixtures.mixins import SupplementModelsFixturesMixin


class SupplementFixtureCreationTests(TestCase, SupplementModelsFixturesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.create_basic_fixtures_from_factory()

    def test_ingredients_creation(self):
        self.assertTrue(self.ingredients)

    def test_default_ingredient(self):
        default_ingredient = self.ingredients[0]

        self.assertEqual(default_ingredient.name, DEFAULT_INGREDIENT_NAME)
        self.assertEqual(default_ingredient.half_life_minutes, DEFAULT_INGREDIENT_HL_MINUTE)
