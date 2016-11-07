# A one-off script that is manually run to look at individual results
from analytics.events.analytics import DataFrameEventsAnalyzer
from importers.excel.importer import ExcelSupplementFileSanitizer

personal_fixtures_file = '/betterself/personal_fixtures/supplement_event_log.xlsx'

sanitizer = ExcelSupplementFileSanitizer(personal_fixtures_file, user=None)
dataframe = sanitizer.get_sanitized_dataframe()

ignore_columns = [
    'Day',
    'Notes',
]

correlation_driver = 'Productivity Time (Minutes)'
# use this to ignore days
rest_day_column_name = 'Rest Day'

analyzer = DataFrameEventsAnalyzer(dataframe, ignore_columns=ignore_columns, rest_day_column_name=rest_day_column_name)
dataframe = analyzer.dataframe

summed_dataframe = analyzer.get_rolled_dataframe(dataframe, 7)

# TD - Create Data fixture that sums up dataframe
# sum function should not accept nulls
# Create datafixture that tests this
simple_results = analyzer.get_correlation_across_summed_days_for_measurement(correlation_driver)
