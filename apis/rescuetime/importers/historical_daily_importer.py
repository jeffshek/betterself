import pandas as pd
import requests

from apis.rescuetime.importers.utils import calculate_rescue_time_pulse_from_dataframe, \
    RESCUETIME_EFFICIENCY_HEADERS, PRODUCTIVITY_PULSE, RESCUETIME_MAPPING_TO_INTERNAL_MODEL
from events.models import DailyProductivityLog

RT_API_URL = 'https://www.rescuetime.com/anapi/data'


class RescueTimeHistoricalDailyImporter(object):
    def __init__(self, user, rescuetime_api_key):
        self.user = user
        self.rescuetime_api_key = rescuetime_api_key
        self.results = pd.DataFrame()

    def import_history(self, start_date, end_date):
        dataframe_columns = RESCUETIME_EFFICIENCY_HEADERS + [PRODUCTIVITY_PULSE]
        historical_df = pd.DataFrame(columns=dataframe_columns)

        query_dates = pd.date_range(start=start_date, end=end_date).date

        for query_date in query_dates:
            response = self._get_rescuetime_efficiency_for_date(query_date)

            if response.status_code != 200:
                continue

            efficiency_timeseries = self.get_efficiency_timeseries_from_response(response)
            pulse = calculate_rescue_time_pulse_from_dataframe(efficiency_timeseries)
            efficiency_timeseries[PRODUCTIVITY_PULSE] = pulse

            # Update the dataframe with history
            historical_df.loc[query_date] = efficiency_timeseries

        # when done, update into the results
        self.results = historical_df

    def save(self):
        # if no valid data, don't save over anything as a safety precaution
        if self.results.empty:
            return

        # save over any productivity logs we might have historically had
        # drop any indices where all the data is null
        valid_dataframe = self.results.dropna(how='all', axis=1)

        # find any overlaps and remove
        old_logs = DailyProductivityLog.objects.filter(user=self.user, date__in=valid_dataframe.index)
        old_logs.delete()

        valid_dataframe.index.name = 'date'
        valid_dataframe = valid_dataframe.rename(columns=RESCUETIME_MAPPING_TO_INTERNAL_MODEL)

        # we don't save productivity pulse
        valid_dataframe = valid_dataframe.drop(PRODUCTIVITY_PULSE, axis=1)

        records = []
        for index, values in valid_dataframe.iterrows():
            values_serialized = values.fillna(0).to_dict()
            log = DailyProductivityLog(
                user=self.user, date=index, source='api',
                **values_serialized
            )
            records.append(log)

        DailyProductivityLog.objects.bulk_create(records)

    def _get_rescuetime_efficiency_for_date(self, query_date):
        query_date_formatted = query_date.strftime('%Y-%m-%d')

        parameters = {
            'key': self.rescuetime_api_key,
            # same date because we just care about one day
            'restrict_begin': query_date_formatted,
            'restrict_end': query_date_formatted,
            'format': 'json',
            'restrict_kind': 'efficiency',
        }

        response = requests.get(RT_API_URL, data=parameters)
        return response

    @staticmethod
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
