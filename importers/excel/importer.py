import pandas as pd


class ExcelXlsxSanitizer(object):
    """Take a raw historical excel file and clean it"""
    IGNORE_COLUMNS = [
        # don't really care about what day of the week for correlations
        'Day',
        'Very Distracting Time'
    ]
    REQUIRED_COLUMNS = [
        'Sleep Time (What you got the night before)',
        'Productivity Time'
    ]
    DATE_COLUMN = 'Date'
    REST_DAY_COLUMN = "Rest Day"

    def __init__(self, file_path, sheet=None):
        self.file_path = file_path
        # Sheet1 is default name for xlsx files
        self.sheet = sheet if sheet else 'Sheet1'

    def get_sanitized_dataframe(self):
        excel_file = pd.ExcelFile(self.file_path)
        dataframe = excel_file.parse(self.sheet)

        # Sanitize so the inputs are correct and then
        # remove any fluke days
        dataframe = self._sanitize_sheet(dataframe)
        dataframe = self._remove_unqualified_data(dataframe)
        dataframe = self._set_dataframe_index(dataframe)

        return dataframe

    def _sanitize_sheet(self, dataframe):
        dataframe = self._sanitize_dataframe_columns(dataframe)
        dataframe = self._sanitize_dataframe_values(dataframe)
        return dataframe

    def _sanitize_dataframe_columns(self, dataframe):
        revised_columns = self._get_cleaned_column_headers(dataframe)
        dataframe = dataframe.rename(columns=revised_columns)

        for column in self.IGNORE_COLUMNS:
            dataframe = dataframe.drop(column, axis=1)

        return dataframe

    def _sanitize_dataframe_values(self, dataframe):
        dataframe = dataframe.replace('T', 1)
        dataframe = dataframe.fillna(0)
        return dataframe

    def _set_dataframe_index(self, dataframe):
        dataframe = dataframe.set_index(dataframe[self.DATE_COLUMN])
        return dataframe

    def _remove_unqualified_data(self, dataframe):
        for column in self.REQUIRED_COLUMNS:
            valid_series = pd.notnull(dataframe[column])
            dataframe = dataframe[valid_series]

        not_rest_days = pd.isnull(dataframe[self.REST_DAY_COLUMN])
        dataframe = dataframe[not_rest_days]

        return dataframe

    @classmethod
    def _get_cleaned_column_headers(cls, dataframe):
        """Return a k/v of crappy columns names without crappy spaces"""
        revised_columns = [item.strip() for item in dataframe.columns]
        updated_columns = dict(zip(dataframe.columns, revised_columns))
        return updated_columns
