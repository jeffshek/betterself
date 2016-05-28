import pandas as pd

from events.models import SupplementProductEventComposition


class ExcelFileSanitizer(object):
    IGNORE_COLUMNS = []

    def __init__(self, file_path, sheet=None):
        self.file_path = file_path
        # Sheet1 is default name for xlsx files
        self.sheet = sheet if sheet else 'Sheet1'

    def get_sanitized_dataframe(self, date_column='DATE'):
        excel_file = pd.ExcelFile(self.file_path)
        dataframe = excel_file.parse(self.sheet)

        # Sanitize so the inputs are correct and then
        # remove any fluke days
        dataframe = self._sanitize_sheet(dataframe)
        dataframe = self._set_dataframe_index(dataframe, date_column)
        return dataframe

    @staticmethod
    def _sanitize_dataframe_values(dataframe):
        dataframe = dataframe.replace('T', 1)
        dataframe = dataframe.fillna(0)
        return dataframe

    @staticmethod
    def _set_dataframe_index(dataframe, date_column):
        dataframe = dataframe.set_index(dataframe[date_column])

        # dump the date_column after settings, shouldn't be used
        # in analysis
        dataframe = dataframe.drop(date_column, axis=1)
        return dataframe

    def _sanitize_sheet(self, dataframe):
        dataframe = self._sanitize_dataframe_columns(dataframe)
        dataframe = self._sanitize_dataframe_values(dataframe)
        return dataframe

    @classmethod
    def _get_cleaned_column_headers(cls, dataframe):
        """Return a k/v of crappy columns names without crappy spaces"""
        revised_columns = [item.strip() for item in dataframe.columns]
        updated_columns = dict(zip(dataframe.columns, revised_columns))
        return updated_columns

    def _sanitize_dataframe_columns(self, dataframe):
        revised_columns = self._get_cleaned_column_headers(dataframe)
        dataframe = dataframe.rename(columns=revised_columns)

        for column in self.IGNORE_COLUMNS:
            dataframe = dataframe.drop(column, axis=1)

        return dataframe


class SupplementSanitizerTemplate(ExcelFileSanitizer):
    """Take a raw historical excel of supplements and clean it"""
    TEMPLATE_SAVE_MODEL = SupplementProductEventComposition

