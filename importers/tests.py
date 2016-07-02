import pandas as pd

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from events.models import SupplementProductEventComposition

from importers.excel.importer import SupplementSanitizerTemplate
# use django user model
from supplements.models import Ingredient, IngredientComposition, MeasurementUnit, SupplementProduct

User = get_user_model()


class ExcelImporterTests(TestCase):
    def setUp(self):
        # create user
        User.objects.create_user(username='jacob', email='jacob@donkey.com', password='top_secret')
        self.user = User.objects.get(username='jacob')

        file_path = settings.ROOT_DIR.path("importers", "fixtures", "tests", "supplement_log_fixtures.xlsx")
        # path is like a command pattern, so we call it now to get the string location
        file_path = file_path()
        self.sanitizer = SupplementSanitizerTemplate(file_path, self.user)

    def test_sanitizer_results_is_dataframe(self):
        results = self.sanitizer.get_sanitized_dataframe()

        results_type = type(results)
        dataframe_type = type(pd.DataFrame())

        self.assertEqual(results_type, dataframe_type)

    def test_supplements_creation_from_sanitizer(self):
        results = self.sanitizer.get_sanitized_dataframe()
        self.sanitizer._create_supplement_products_from_dataframe(results)

        # all these would be created by a test use from fixtures
        ingredient_exists = Ingredient.objects.all().exists()
        mu_exists = MeasurementUnit.objects.all().exists()
        ing_comp_exists = IngredientComposition.objects.all().exists()
        supplement_products_exists = SupplementProduct.objects.all().exists()

        self.assertTrue(ingredient_exists)
        self.assertTrue(mu_exists)
        self.assertTrue(ing_comp_exists)
        self.assertTrue(supplement_products_exists)

    def test_fixtures_import(self):
        results = self.sanitizer.get_sanitized_dataframe()
        self.sanitizer.save_results(results)

        supplement_events_exist = SupplementProductEventComposition.objects.all().exists()
        self.assertTrue(supplement_events_exist)

    def test_get_measurement_unit_and_quantity_from_name(self):
        test_name_1 = 'Snake Oil (200mg)'
        result = SupplementSanitizerTemplate.get_measurement_unit_and_quantity_from_name(test_name_1)

        self.assertEqual(result['quantity'], 200)

        test_name_2 = 'Snake Oil'
        result = SupplementSanitizerTemplate.get_measurement_unit_and_quantity_from_name(test_name_2)
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
