import datetime

import pandas as pd
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from django.test import TestCase

from events.models import SupplementEvent
from importers.serializers.excel.serializers import ExcelSupplementFileSerializer
from supplements.models import Ingredient, IngredientComposition, Measurement, Supplement

User = get_user_model()

# python manage.py test importers.tests.test_serializers


class ExcelImporterTests(LiveServerTestCase, TestCase):
    file_path = settings.ROOT_DIR.path('importers', 'fixtures', 'tests', 'supplement_log_fixtures.xlsx')

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='jacob', email='jacob@donkey.com', password='top_secret')
        cls.user = User.objects.get(username='jacob')

        file_path = cls.file_path()
        cls.sanitizer = ExcelSupplementFileSerializer(file_path, cls.user)

        super().setUpTestData()

    def test_sanitizer_results_is_dataframe(self):
        results = self.sanitizer.get_sanitized_dataframe()

        results_type = type(results)
        dataframe_type = type(pd.DataFrame())

        self.assertEqual(results_type, dataframe_type)

    def test_supplements_dont_natively_exist(self):
        # paranoid that i might mess up something one day
        supplement_exists = Supplement.objects.all().exists()
        self.assertFalse(supplement_exists)

    def test_supplements_creation_from_sanitizer(self):
        results = self.sanitizer.get_sanitized_dataframe()
        self.sanitizer._create_supplements_from_dataframe(results)

        # all these would be created by a test use from fixtures
        ingredient_exists = Ingredient.objects.all().exists()
        mu_exists = Measurement.objects.all().exists()
        ing_comp_exists = IngredientComposition.objects.all().exists()
        supplement_exists = Supplement.objects.all().exists()

        self.assertTrue(ingredient_exists)
        self.assertTrue(mu_exists)
        self.assertTrue(ing_comp_exists)
        self.assertTrue(supplement_exists)

    def test_fixtures_import(self):
        supplement_events_dont_exist_yet = SupplementEvent.objects.all().exists()
        self.assertFalse(supplement_events_dont_exist_yet)

        # this is kind of a crappy test, but i'm just using implicit knowledge of fixtures
        # to test that the entries created are correct
        results = self.sanitizer.get_sanitized_dataframe()
        self.sanitizer.save_results(results)

        supplement_events_exist = SupplementEvent.objects.all().exists()
        self.assertTrue(supplement_events_exist)

    def test_get_measurement_unit_and_quantity_from_name(self):
        test_name_1 = 'Snake Oil (200mg)'
        result = ExcelSupplementFileSerializer._get_measurement_and_quantity_from_name(test_name_1, 'random_uuid')

        self.assertEqual(result['quantity'], 200)

        test_name_2 = 'Snake Oil'
        result = ExcelSupplementFileSerializer._get_measurement_and_quantity_from_name(test_name_2, 'random_uuid')
        result_quantity = result.get('quantity')

        self.assertEqual(result_quantity, 1)

    def test_columns_with_spaces_in_excel(self):
        series = pd.Series([1, 2, 3])
        dataframe = pd.DataFrame(
            {
                '               A': series,  # make some ridiculous columns
                '               B (200mg)': series,
            }
        )

        cleaned_dataframe = ExcelSupplementFileSerializer.sanitize_dataframe_columns(dataframe)
        cleaned_columns = cleaned_dataframe.columns

        self.assertTrue('A' in cleaned_columns)
        self.assertTrue('B (200mg)' in cleaned_columns)
        self.assertFalse('               A' in cleaned_columns)

    def test_true_strings_get_validated_to_one(self):
        # Correlations don't work for strings labelled as True, duh
        supplement_name = 'Random Supplement'
        true_string_names = ['True', 'true', 't', 'T']
        values_to_create = 50

        for true_string_name in true_string_names:
            serialized_dataframe = self._get_serialized_dataframe(supplement_name, true_string_name, values_to_create)

            # if creating true/false, those result in 1 or 0s ...
            series_sum = serialized_dataframe[supplement_name].sum()
            self.assertEqual(1 * values_to_create, series_sum)

    def test_false_strings_get_validated_to_one(self):
        # Correlations don't work for strings labelled as True, duh
        supplement_name = 'Random Supplement'
        false_string_names = ['False', 'false', 'f', 'F']
        values_to_create = 50

        for string_name in false_string_names:
            serialized_dataframe = self._get_serialized_dataframe(supplement_name, string_name, values_to_create)

            # if creating true/false, those result in 1 or 0s ...
            series_sum = serialized_dataframe[supplement_name].sum()
            self.assertEqual(0, series_sum)

    def _get_serialized_dataframe(self, supplement_name, boolean_string_name, values_to_create):
        data_values = [boolean_string_name] * values_to_create
        today = datetime.date.today()
        periods_ago = today - datetime.timedelta(days=values_to_create - 1)
        date_range = pd.date_range(periods_ago, today)

        # this would be stupid if the count is off
        self.assertEqual(len(data_values), len(date_range))

        dataframe = pd.DataFrame(index=date_range)
        dataframe[supplement_name] = data_values

        # make sure there's no dynamic type conversion that can screw you
        series = dataframe[supplement_name]
        self.assertEqual(series[0], boolean_string_name)

        serialized_dataframe = ExcelSupplementFileSerializer._sanitize_dataframe_values(dataframe)
        return serialized_dataframe
