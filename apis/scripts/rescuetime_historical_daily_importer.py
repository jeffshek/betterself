import datetime

import requests
from dateutil import relativedelta
from django.conf import settings
import pandas as pd

# No nesting allowed!
# Really annoying aspect of runscript is it only runs from app/scripts folder
from apis.rescuetime.utils.importer import calculate_rescue_time_pulse_from_dataframe, \
    RESCUETIME_EFFICIENCY_HEADERS, PRODUCTIVITY_PULSE

RT_API_KEY = settings.RESCUETIME_API_KEY
RT_API_URL = 'https://www.rescuetime.com/anapi/data'

# python manage.py runscript rescuetime_historical_daily_importer


def get_rescuetime_efficiency_response_for_dates(restrict_begin, restrict_end):
    restrict_begin_formatted = restrict_begin.strftime('%Y-%m-%d')
    restrict_end_formatted = restrict_end.strftime('%Y-%m-%d')

    parameters = {
        'key': RT_API_KEY,
        'restrict_begin': restrict_begin_formatted,
        'restrict_end': restrict_end_formatted,
        'format': 'json',
        'restrict_kind': 'efficiency',

    }
    response = requests.get(RT_API_URL, data=parameters)

    return response


def run(*args):
    # Used as a simple way to see your own scores from RescueTime
    # and do aggregate analysis on it
    dataframe_columns = RESCUETIME_EFFICIENCY_HEADERS + [PRODUCTIVITY_PULSE]
    historical_df = pd.DataFrame(columns=dataframe_columns)

    end_date = datetime.date(2017, 5, 31)
    days_to_look_back = 60

    for days_back in range(0, days_to_look_back):
        lookup_date = end_date - relativedelta.relativedelta(days=days_back)
        response = get_rescuetime_efficiency_response_for_dates(
            # same because we just care about one day
            restrict_begin=lookup_date,
            restrict_end=lookup_date,
        )

        efficiency_timeseries = get_efficiency_timeseries_from_response(response)
        pulse = calculate_rescue_time_pulse_from_dataframe(efficiency_timeseries)
        efficiency_timeseries[PRODUCTIVITY_PULSE] = pulse

        # Update the dataframe with history
        historical_df.loc[lookup_date] = efficiency_timeseries

    # A bit of a hack, but just output to path
    historical_df.to_csv('historical_rescuetime.csv')


def get_efficiency_timeseries_from_response(response):
    json_data = response.json()

    columns = json_data['row_headers']
    data = json_data['rows']

    # we get a bunch of useless data, so massage the data to what we need
    """
           Rank  Time Spent (seconds)  Number of People             Efficiency
    0     1                 33791                 1         Very Productive Time
    1     2                  4869                 1         Distracting Time
    2     3                  1567                 1         Very Distracting Time
    3     4                  1132                 1         Productive Time
    4     5                   585                 1         Neutral Time
    """
    parsed_dataframe = pd.DataFrame(columns=columns, data=data)
    parsed_timeseries = pd.Series(
        index=parsed_dataframe['Efficiency'].values,
        data=parsed_dataframe['Time Spent (seconds)'].values
    )

    # convert seconds to minutes
    parsed_timeseries = parsed_timeseries / 60

    return parsed_timeseries
