import pandas as pd

from analytics.events.utils.dataframe_builders import SupplementEventsDataframeBuilder, \
    ProductivityLogEventsDataframeBuilder, UserActivityEventDataframeBuilder, SleepActivityDataframeBuilder
from events.models import SupplementEvent, DailyProductivityLog, UserActivityLog, SleepActivity


class AggregateDataFrameBuilder(object):
    def __init__(
            self,
            user_activities_events_queryset,
            productivity_log_queryset,
            supplement_event_queryset,
            sleep_activities_queryset
    ):
        # Have a dataframe builder that can accept a multiple set of kwargs that way we can one generic dataframe
        # builder that can accept multiple different format
        self.user_activities_events_queryset = user_activities_events_queryset
        self.productivity_log_queryset = productivity_log_queryset
        self.supplement_event_queryset = supplement_event_queryset
        self.sleep_activities_queryset = sleep_activities_queryset

    @staticmethod
    def get_supplement_event_dataframe(queryset):
        builder = SupplementEventsDataframeBuilder(queryset)
        supplement_event_dataframe = builder.get_flat_daily_dataframe()
        return supplement_event_dataframe

    @staticmethod
    def get_productivity_log_dataframe(queryset):
        builder = ProductivityLogEventsDataframeBuilder(queryset)
        productivity_log_dataframe = builder.build_dataframe()
        return productivity_log_dataframe

    @staticmethod
    def get_sleep_activity_series(queryset):
        builder = SleepActivityDataframeBuilder(queryset)
        series = builder.get_sleep_history_series()
        return series

    @staticmethod
    def get_user_activity_events_dataframe(queryset):
        builder = UserActivityEventDataframeBuilder(queryset)
        user_activity_dataframe = builder.get_flat_daily_dataframe()
        return user_activity_dataframe

    def build_daily_dataframe(self):
        # if a queryset is passed, attempt to build a dataframe from the queryset
        # and then concat all the dataframes in the array
        contact_dfs = []

        if self.user_activities_events_queryset:
            df = self.get_user_activity_events_dataframe(self.user_activities_events_queryset)
            contact_dfs.append(df)

        if self.productivity_log_queryset:
            df = self.get_productivity_log_dataframe(self.productivity_log_queryset)
            contact_dfs.append(df)

        if self.supplement_event_queryset:
            df = self.get_supplement_event_dataframe(self.supplement_event_queryset)
            contact_dfs.append(df)

        if self.sleep_activities_queryset:
            df = self.get_sleep_activity_series(self.sleep_activities_queryset)
            contact_dfs.append(df)

        # axis of zero means to align them based on column we want to align it based on matching index, so axis=1
        # this seems kind of weird though for axis of 1 to mean the index though
        if contact_dfs:
            concat_df = pd.concat(contact_dfs, axis=1)
        else:
            # concat doesn't work with an empty list, in the case of no data, return empty dataframe
            concat_df = pd.DataFrame()

        return concat_df


class AggregateSleepActivitiesUserActivitiesBuilder(AggregateDataFrameBuilder):
    def __init__(self, user_activities_events_queryset, sleep_activities_queryset):
        super().__init__(
            user_activities_events_queryset=user_activities_events_queryset,
            productivity_log_queryset=None,
            supplement_event_queryset=None,
            sleep_activities_queryset=sleep_activities_queryset,
        )

    @classmethod
    def get_aggregate_dataframe_for_user(cls, user, cutoff_date=None):
        user_activity_events = UserActivityLog.objects.filter(user=user)
        sleep_logs = SleepActivity.objects.filter(user=user)

        if cutoff_date:
            user_activity_events = user_activity_events.filter(time__gte=cutoff_date)
            sleep_logs = sleep_logs.filter(start_time__gte=cutoff_date)

        aggregate_dataframe = cls(
            user_activities_events_queryset=user_activity_events,
            sleep_activities_queryset=sleep_logs
        )

        dataframe = aggregate_dataframe.build_daily_dataframe()
        return dataframe


class AggregateSleepActivitiesSupplementsBuilder(AggregateDataFrameBuilder):
    def __init__(self, sleep_activities_queryset, supplement_event_queryset):
        super().__init__(
            user_activities_events_queryset=None,
            productivity_log_queryset=None,
            supplement_event_queryset=supplement_event_queryset,
            sleep_activities_queryset=sleep_activities_queryset,
        )

    @classmethod
    def get_aggregate_dataframe_for_user(cls, user, cutoff_date=None):
        sleep_logs = SleepActivity.objects.filter(user=user)
        supplement_events = SupplementEvent.objects.filter(user=user)

        if cutoff_date:
            sleep_logs = sleep_logs.filter(start_time__gte=cutoff_date)
            supplement_events = supplement_events.filter(time__gte=cutoff_date)

        aggregate_dataframe = cls(
            sleep_activities_queryset=sleep_logs,
            supplement_event_queryset=supplement_events
        )

        dataframe = aggregate_dataframe.build_daily_dataframe()
        return dataframe


class AggregateUserActivitiesEventsProductivityActivitiesBuilder(AggregateDataFrameBuilder):
    def __init__(self, user_activities_events_queryset, productivity_log_queryset):
        super().__init__(
            user_activities_events_queryset=user_activities_events_queryset,
            productivity_log_queryset=productivity_log_queryset,
            supplement_event_queryset=None,
            sleep_activities_queryset=None
        )

    @classmethod
    def get_aggregate_dataframe_for_user(cls, user, cutoff_date=None):
        user_activity_events = UserActivityLog.objects.filter(user=user)
        productivity_logs = DailyProductivityLog.objects.filter(user=user)

        if cutoff_date:
            user_activity_events = user_activity_events.filter(time__gte=cutoff_date)
            productivity_logs = productivity_logs.filter(date__gte=cutoff_date)

        aggregate_dataframe = cls(
            user_activities_events_queryset=user_activity_events,
            productivity_log_queryset=productivity_logs,
        )

        dataframe = aggregate_dataframe.build_daily_dataframe()
        return dataframe


class AggregateSupplementProductivityDataframeBuilder(AggregateDataFrameBuilder):
    def __init__(self, supplement_event_queryset, productivity_log_queryset):
        super().__init__(
            supplement_event_queryset=supplement_event_queryset,
            productivity_log_queryset=productivity_log_queryset,
            user_activities_events_queryset=None,
            sleep_activities_queryset=None
        )

    @classmethod
    def get_aggregate_dataframe_for_user(cls, user, cutoff_date=None):
        supplement_events = SupplementEvent.objects.filter(user=user)
        productivity_logs = DailyProductivityLog.objects.filter(user=user)

        if cutoff_date:
            supplement_events = supplement_events.filter(time__gte=cutoff_date)
            productivity_logs = productivity_logs.filter(date__gte=cutoff_date)

        aggregate_dataframe = cls(
            supplement_event_queryset=supplement_events,
            productivity_log_queryset=productivity_logs,
        )
        dataframe = aggregate_dataframe.build_daily_dataframe()
        return dataframe
