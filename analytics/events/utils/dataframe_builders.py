import numpy as np
import pandas as pd

from betterself.utils.pandas_utils import get_empty_timezone_aware_series_containing_index_of_today
from constants import SLEEP_CUTOFF_TIME, SLEEP_MINUTES_COLUMN, VERY_PRODUCTIVE_TIME_LABEL, PRODUCTIVE_TIME_LABEL, \
    NEUTRAL_TIME_LABEL, DISTRACTING_TIME_LABEL, VERY_DISTRACTING_TIME_LABEL

SOURCE_COLUMN_NAME = 'Source'
QUANTITY_COLUMN_NAME = 'Quantity'
SUPPLEMENT_COLUMN_NAME = 'Supplement'
TIME_COLUMN_NAME = 'Time'

SUPPLEMENT_EVENT_COLUMN_MAP = {
    'source': SOURCE_COLUMN_NAME,
    'supplement__name': SUPPLEMENT_COLUMN_NAME,
    'quantity': QUANTITY_COLUMN_NAME,
    'time': TIME_COLUMN_NAME,
}


DATE_LABEL = 'Date'

PRODUCTIVITY_LOG_COLUMN_MAP = {
    'source': SOURCE_COLUMN_NAME,
    'date': DATE_LABEL,
    'very_productive_time_minutes': VERY_PRODUCTIVE_TIME_LABEL,
    'productive_time_minutes': PRODUCTIVE_TIME_LABEL,
    'neutral_time_minutes': NEUTRAL_TIME_LABEL,
    'distracting_time_minutes': DISTRACTING_TIME_LABEL,
    'very_distracting_time_minutes': VERY_DISTRACTING_TIME_LABEL,
}


class DataFrameBuilder(object):
    rename_columns = True

    def build_dataframe(self):
        if not self.values.exists():
            return pd.DataFrame()

        # Am I really a programmer or just a lego assembler?
        # Pandas makes my life at least 20 times easier.
        df = pd.DataFrame.from_records(self.values, index=self.index_column)

        # make the columns and labels prettier
        if self.rename_columns:
            df = df.rename(columns=self.column_mapping)

        df.index.name = TIME_COLUMN_NAME
        try:
            df.index = df.index.tz_convert(self.user.pytz_timezone)
        except AttributeError:
            # if attribute-error means the index is just a regular Index and
            # that only dates (and not time) was passed
            df.index = pd.DatetimeIndex(df.index, tz=self.user.pytz_timezone)

        # cast it as numerics if possible, otherwise if we're dealing with strings, ignore
        df = df.apply(pd.to_numeric, errors='ignore')

        return df


class SupplementEventsDataframeBuilder(DataFrameBuilder):
    """
    Builds a pandas dataframe from a SupplementLog queryset ... once we get to a dataframe
    analytics are just super easy to work with and we can do a lot of complex analysis on top of it
    """
    index_column = 'time'
    column_mapping = SUPPLEMENT_EVENT_COLUMN_MAP

    def __init__(self, queryset):
        queryset = queryset.select_related('supplement')
        self.queryset = queryset
        values_columns = self.column_mapping.keys()
        # tell the queryset to only specifically get a set of columns are about
        self.values = self.queryset.values(*values_columns)

        try:
            self.user = self.queryset[0].user
        except IndexError:
            self.user = None

    def get_flat_daily_dataframe(self):
        """
        Simplify the history of whatever supplements were taken - round the timestamps
        to dates and then sum the # taken up per supplement.

        If a start or end date are passed, assume that that index expects on aggregation to include up to those dates
        so if the data stops on 6-5-2017 but the end date is 6-10-2017, there would be records on 6-6, 6-7, etc saying
        no data, nan, etc.
        """
        df = self.build_dataframe()
        if df.empty:
            return df

        flat_df = self._get_summed_df_by_daily_index(df, timezone=self.user.pytz_timezone)
        return flat_df

    @staticmethod
    def _get_summed_df_by_daily_index(df, timezone):
        # switch the index to something generic like a date so that we can sum daily iterations
        df.index = df.index.date

        flat_df = df.pivot_table(
            index=df.index,
            values=QUANTITY_COLUMN_NAME,
            columns=SUPPLEMENT_COLUMN_NAME,
            aggfunc=np.sum
        )

        # When doing a pivot, the dataframe type seems to convert from float64 back to object ... convert to float64
        flat_df = flat_df.astype('float64')

        # ensure a sort because if out of order, casting frequencies silently fails
        flat_df = flat_df.sort_index()

        # Set as a daily frequency and set it back to a timezone aware date
        flat_df = flat_df.asfreq('D')

        flat_df = flat_df.tz_localize(timezone)

        return flat_df


class ProductivityLogEventsDataframeBuilder(DataFrameBuilder):
    index_column = 'date'
    column_mapping = PRODUCTIVITY_LOG_COLUMN_MAP

    def __init__(self, queryset, rename_columns=True):
        self.rename_columns = rename_columns

        self.queryset = queryset
        values_columns = self.column_mapping.keys()
        self.values = self.queryset.values(*values_columns)

        try:
            self.user = self.queryset[0].user
        except IndexError:
            self.user = None

    def get_flat_daily_dataframe(self):
        """
        Simplify the history of the model and condense it to a daily metric
        """
        df = self.build_dataframe()
        # ProductivityLogs are already in a daily format, so no need to flatten
        return df

    def get_productive_timeseries(self):
        df = self.build_dataframe()

        # get a list of the columns that indicate productivity
        # in the future, potentially weight these differently
        productive_columns = [item for item in df.keys() if 'Productive' in item]
        productive_df = df[productive_columns]

        # now sum all the columns together to get a sum of collective periods
        productive_timeseries = productive_df.sum(axis=1)

        return productive_timeseries

    def get_unproductive_timeseries(self):
        df = self.build_dataframe()

        # get a list of the columns that indicate productivity that isn't
        unproductive_columns = [
            item for item in df.keys()
            if 'Productive' not in item
               and 'Minutes' in item
        ]
        # exclude "source" too
        unproductive_df = df[unproductive_columns]

        # now sum all the columns together to get a sum of collective periods
        unproductive_timeseries = unproductive_df.sum(axis=1)
        return unproductive_timeseries


class SleepActivityDataframeBuilder(object):
    """
    Custom serializer to parse sleep logs in a meaningful way

    Returns a dataframe of sleep activity
    """

    def __init__(self, queryset, user=None, rename_columns=True):
        self.rename_columns = rename_columns

        self.sleep_activities = queryset

        if user:
            self.user = user
        else:
            try:
                self.user = self.sleep_activities[0].user
            except IndexError:
                self.user = None

    @staticmethod
    def round_timestamp_to_sleep_date(timeseries):
        """
        Not my proudest function ... this isn't as efficient as it could be, but struggling
        with some pandas syntax to find the perfect pandas one-line

        This can be much more performant, but need time to sit down and figure it out
        """
        sleep_dates = []
        for value in timeseries:
            if value.hour < SLEEP_CUTOFF_TIME:
                result = value - pd.DateOffset(days=1)
            else:
                result = value

            sleep_dates.append(result)

        index = pd.DatetimeIndex(sleep_dates)
        return index

    def get_sleep_history_series(self):
        """
        Think of this as Sleep ON. Sleep ON that date.

        This returns data as how much sleep did you sleep on Monday night?

        So if you sleep from Monday 10PM to Tuesday 3AM, this will report Monday as 5 Hours! However, this can look
        weird in a graph as being a day off.
        """
        # TODO - Fix this lame hack
        if not self.user:
            return pd.Series()

        if not self.sleep_activities.exists():
            index = get_empty_timezone_aware_series_containing_index_of_today(self.user)
            return pd.Series(index=index)

        user_timezone = self.user.pytz_timezone

        sleep_activities_values = self.sleep_activities.values('start_time', 'end_time')
        sleep_activity_normalized_timezones = []
        for record in sleep_activities_values:
            record_normalized = {key: user_timezone.normalize(value) for key, value in record.items()}
            sleep_activity_normalized_timezones.append(record_normalized)

        # for each given 24 hour period (ending at 11AM)
        # Lot of mental debate here between calculating the sleep one gets from monday 10PM to tuesday 6AM which
        # date it should be attributed to ... aka either a Monday or Tuesday night.
        # I've decided to lean toward calculating that as Monday night
        dataframe = pd.DataFrame.from_records(sleep_activity_normalized_timezones)
        dataframe['sleep_time'] = dataframe['end_time'] - dataframe['start_time']

        sleep_index = self.round_timestamp_to_sleep_date(dataframe['end_time'])
        sleep_series = pd.Series(dataframe['sleep_time'].values, index=sleep_index)

        # get the sum of time slept during days (so this includes naps)
        # the result is timedeltas though, so convert below
        sleep_aggregate = sleep_series.resample('D').sum()

        # change from timedeltas to minutes, otherwise json response of timedelta is garbage
        sleep_aggregate = sleep_aggregate / np.timedelta64(1, 'm')
        sleep_aggregate.name = SLEEP_MINUTES_COLUMN
        return sleep_aggregate


class UserActivityEventDataframeBuilder(object):
    def __init__(self, queryset):
        self.user_activities = queryset

        try:
            self.user = self.user_activities[0].user
        except IndexError:
            self.user = None

    def get_flat_daily_dataframe(self):
        activity_events_values = self.user_activities.values('time', 'user_activity__name')

        if not self.user:
            return pd.DataFrame()

        user_timezone = self.user.pytz_timezone

        time_index = [item['time'].astimezone(user_timezone).date() for item in activity_events_values]
        time_index_localized = pd.DatetimeIndex(time_index).tz_localize(user_timezone)
        activity_names = [item['user_activity__name'] for item in activity_events_values]

        df = pd.DataFrame({
            'time': time_index_localized,
            'activity': activity_names,
            # value of 1 since we only allow one event to occur at a particular time
            'value': 1
        })

        # switch to a flattened history of user activity dataframe instead
        df = df.pivot_table(index=pd.DatetimeIndex(df['time']), values='value', columns='activity', aggfunc=np.sum)
        df = df.asfreq('D')

        # so the column doesn't look as bad in an output
        df.index.name = 'Date'

        return df
