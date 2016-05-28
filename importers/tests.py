import pandas as pd

from django.test import TestCase

from importers.excel.importer import SupplementSanitizerTemplate


class ExcelImporterTests(TestCase):
    def test_excel_importer(self):
        file_path = 'fixtures/tests/supplement_log_fixtures.xslx'
        sanitizer = SupplementSanitizerTemplate(file_path)
        results = sanitizer.get_sanitized_dataframe()

        results_type = type(results)
        dataframe_type = type(pd.DataFrame())

        self.assertEqual(results_type, dataframe_type)


# TD
# Make sure all columns (ie. no "    Advil" is saved, always check strip).
