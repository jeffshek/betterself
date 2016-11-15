# A one-off script that is run (manually) to look at individual results
from analytics.events.analytics import DataFrameEventsAnalyzer
from importers.excel.importer import ExcelSupplementFileSanitizer
import pandas as pd

personal_fixtures_file = '/betterself/personal_fixtures/supplement_event_log.xlsx'

sanitizer = ExcelSupplementFileSanitizer(personal_fixtures_file, user=None, sheet='Log')
dataframe = sanitizer.get_sanitized_dataframe()

ignore_columns = [
    'Day',
    'Notes',
]

correlation_driver = 'Productivity Time (Minutes)'
# use this to ignore days
rest_day_column_name = 'Rest Day'

analyzer = DataFrameEventsAnalyzer(dataframe, ignore_columns=ignore_columns, rest_day_column=rest_day_column_name)
dataframe = analyzer.dataframe
dataframe_with_yesterday = analyzer.add_yesterday_shifted_to_dataframe(dataframe)

# get a list of any value that isn't a zero that should be counted
event_count = analyzer.get_dataframe_event_count(dataframe_with_yesterday)

results = (analyzer.get_correlation_across_summed_days_for_measurement(measurement=correlation_driver,
    add_yesterday_lag=True))
results.to_csv('output.csv')

results_with_counts = pd.DataFrame(data={
    'correlation': results,
    'count': event_count
})

results_with_counts = results_with_counts.sort_values(['correlation'])

counts_greater_than_20 = results_with_counts['count'] > 20

results_with_counts = results_with_counts[counts_greater_than_20]
results_with_counts.to_csv('output.csv')
