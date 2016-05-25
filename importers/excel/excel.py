# -*- coding: utf-8 -*-
import pandas as pd

# Not every column is necessary
DISREGARD_COLUMNS = [
    'Day', # don't really care about what day of the week for correlations
    'Very Distracting Time'
]

DATE_COLUMN = 'Date'
REST_DAY_COLUMN = "Rest Day"
REQUIRED_COLUMNS = [
    'Sleep Time (What you got the night before)',
    'Productivity Time'
]

# column you care the most about improving
# DRIVER = ['Sleep Time Minutes']
DRIVER = ['Productivity Time (Minutes)']
# DRIVER = ['Distracting Time (Minutes)']

# lots of personal formatting to look pretty in excel, but code doesn't care about pretty
def clean_and_rename_dataframe_columns(dataframe):
    revised_columns = [item.strip() for item in dataframe.columns]
    update_columns = dict(zip(dataframe.columns, revised_columns))
    dataframe = dataframe.rename(columns=update_columns)

    for column in DISREGARD_COLUMNS:
        dataframe = dataframe.drop(column, axis=1)

    return dataframe


def sanitize_input_data(dataframe):
    dataframe = dataframe.replace('T', 1)
    dataframe = dataframe.fillna(0)
    return dataframe


def remove_unqualified_data(dataframe):
    for column in REQUIRED_COLUMNS:
        valid_series = pd.notnull(dataframe[column])
        dataframe = dataframe[valid_series]

    not_rest_days = pd.isnull(dataframe[REST_DAY_COLUMN])
    dataframe = dataframe[not_rest_days]

    return dataframe


def set_dataframe_index(dataframe):
    dataframe = dataframe.set_index(dataframe[DATE_COLUMN])
    return dataframe


# read fixtures file
historical_dataframe = pd.ExcelFile('personal_fixtures/supplements_fixtures.xlsx').parse('Sheet1', skiprows=1)
historical_dataframe = clean_and_rename_dataframe_columns(historical_dataframe)
historical_dataframe = remove_unqualified_data(historical_dataframe)
historical_dataframe = set_dataframe_index(historical_dataframe)
historical_dataframe = sanitize_input_data(historical_dataframe)

# take a look at anything that has a high correlation
correlation_results = historical_dataframe.corr()[DRIVER].dropna().sort_values(DRIVER, ascending=False)
# historical_dataframe.to_excel('test.xlsx')


