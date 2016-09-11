import pandas as pd

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from events.models import SupplementEvent

from importers.excel.importer import SupplementSanitizerTemplate
# use django user model
from supplements.models import Ingredient, IngredientComposition, Measurement, Supplement

User = get_user_model()


class ExcelImporterTests(TestCase):
    file_path = settings.ROOT_DIR.path('importers', 'fixtures', 'tests', 'supplement_log_fixtures.xlsx')

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='jacob', email='jacob@donkey.com', password='top_secret')
        cls.user = User.objects.get(username='jacob')

        file_path = cls.file_path()
        cls.sanitizer = SupplementSanitizerTemplate(file_path, cls.user)

        super().setUpTestData()

    def test_sanitizer_results_is_dataframe(self):
        results = self.sanitizer.get_sanitized_dataframe()

        results_type = type(results)
        dataframe_type = type(pd.DataFrame())

        self.assertEqual(results_type, dataframe_type)

    def test_supplement_products_dont_natively_exist(self):
        # paranoid that i might mess up something one day
        supplement_products_exists = Supplement.objects.all().exists()
        self.assertFalse(supplement_products_exists)

    def test_supplements_creation_from_sanitizer(self):
        results = self.sanitizer.get_sanitized_dataframe()
        self.sanitizer._create_supplement_products_from_dataframe(results)

        # all these would be created by a test use from fixtures
        ingredient_exists = Ingredient.objects.all().exists()
        mu_exists = Measurement.objects.all().exists()
        ing_comp_exists = IngredientComposition.objects.all().exists()
        supplement_products_exists = Supplement.objects.all().exists()

        self.assertTrue(ingredient_exists)
        self.assertTrue(mu_exists)
        self.assertTrue(ing_comp_exists)
        self.assertTrue(supplement_products_exists)

    def test_fixtures_import(self):
        # this is kind of a crappy test, but i'm just using implicit knowledge of fixtures
        # to test that the entries created are correct
        results = self.sanitizer.get_sanitized_dataframe()
        self.sanitizer.save_results(results)

        supplement_events_exist = SupplementEvent.objects.all().exists()
        self.assertTrue(supplement_events_exist)

    def test_get_measurement_unit_and_quantity_from_name(self):
        test_name_1 = 'Snake Oil (200mg)'
        result = SupplementSanitizerTemplate.get_measurement_and_quantity_from_name(test_name_1)

        self.assertEqual(result['quantity'], 200)

        test_name_2 = 'Snake Oil'
        result = SupplementSanitizerTemplate.get_measurement_and_quantity_from_name(test_name_2)
        result_quantity = result.get('quantity')

        self.assertEqual(result_quantity, None)

    def test_columns_with_spaces_in_excel(self):
        series = pd.Series([1, 2, 3])
        dataframe = pd.DataFrame(
            {
                '               A': series,  # make some ridiculous columns
                '               B (200mg)': series,
            }
        )

        cleaned_dataframe = SupplementSanitizerTemplate._sanitize_dataframe_columns(dataframe)
        cleaned_columns = cleaned_dataframe.columns

        self.assertTrue('A' in cleaned_columns)
        self.assertTrue('B (200mg)' in cleaned_columns)
        self.assertFalse('               A' in cleaned_columns)
