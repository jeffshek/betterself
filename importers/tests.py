import pandas as pd

from django.test import TestCase
from django.contrib.auth import get_user_model

from importers.excel.importer import SupplementSanitizerTemplate

# use django user model
User = get_user_model()


class ExcelImporterTests(TestCase):
    def setUp(self):

        # create user
        User.objects.create_user(username='jacob', email='jacob@donkey.com', password='top_secret')
        self.user = User.objects.get(username='jacob')

    def test_excel_importer(self):
        file_path = '/sites/betterself/importers/fixtures/tests/supplement_log_fixtures.xlsx'

        sanitizer = SupplementSanitizerTemplate(file_path, self.user)
        results = sanitizer.get_sanitized_dataframe()

        results_type = type(results)
        dataframe_type = type(pd.DataFrame())

        self.assertEqual(results_type, dataframe_type)

    def test_get_measurement_unit_and_quantity_from_name(self):
        test_name_1 = 'Snake Oil (200mg)'
        result = SupplementSanitizerTemplate.get_measurement_unit_and_quantity_from_name(test_name_1)
        self.assertEqual(result['quantity'], 200)

        test_name_2 = 'Snake Oil'
        result = SupplementSanitizerTemplate.get_measurement_unit_and_quantity_from_name(test_name_2)
        self.assertEqual(result['quantity'], None)


# TD
# Make sure all columns (ie. no "    Advil" is saved, always check strip).
