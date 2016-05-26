import pandas as pd

from django.test import TestCase


class ExcelImporterTests(TestCase):
    def setUp(cls):
        """
        Not always necessary
        """
        pass

    def test_excel_importer(self):
        excel_file = pd.ExcelFile('fixtures/tests/historical_events.xslx')
        return
