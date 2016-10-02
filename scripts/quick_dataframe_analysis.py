from importers.excel.importer import ExcelSupplementFileSanitizer

personal_fixtures_file = '/betterself/personal_fixtures/supplement_fixtures.xlsx'

sanitizer = ExcelSupplementFileSanitizer(personal_fixtures_file, user=None)
dataframe = sanitizer.get_sanitized_dataframe()

dataframe_cols = dataframe.columns

ignore_columns = [
    'Day',
    'Notes',
]

pretty_columns = [item for item in dataframe_cols if item not in ignore_columns]
dataframe = dataframe[pretty_columns]

for col in pretty_columns:
    shifted_col_name = 'Yesterday - {0}'.format(col)
    series = dataframe[col]
    shifted_series = series.shift(1)

    dataframe[shifted_col_name] = shifted_series

correlation_driver = 'Productivity Time (Minutes)'
# correlation_driver = "Productivity Score"

correlation_results = dataframe.corr()[correlation_driver]
correlation_results_sorted = correlation_results.sort_values(inplace=False)

yesterday_cols = [item for item in dataframe.columns if 'Yesterday' in item]
yesterday_correlations = correlation_results_sorted[yesterday_cols]
yesterday_correlations = yesterday_correlations.sort_values(inplace=False)
