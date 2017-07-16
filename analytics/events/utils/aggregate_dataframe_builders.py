import pandas as pd

from analytics.events.utils.dataframe_builders import SupplementEventsDataframeBuilder, \
    ProductivityLogEventsDataframeBuilder
from events.models import SupplementEvent, DailyProductivityLog


class AggregateDataFrameMixin(object):
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


class AggregateSupplementProductivityDataframeBuilder(AggregateDataFrameMixin):
    def __init__(self, supplement_event_queryset, productivity_log_queryset):
        self.supplement_event_queryset = supplement_event_queryset
        self.productivity_log_queryset = productivity_log_queryset

    @classmethod
    def get_aggregate_dataframe_for_user(cls, user):
        supplement_events = SupplementEvent.objects.filter(user=user)
        productivity_log = DailyProductivityLog.objects.filter(user=user)

        aggregate_dataframe = cls(
            supplement_event_queryset=supplement_events,
            productivity_log_queryset=productivity_log,
        )
        dataframe = aggregate_dataframe.build_daily_dataframe()
        return dataframe

    def build_daily_dataframe(self):
        productivity_log_dataframe = self.get_productivity_log_dataframe(self.productivity_log_queryset)
        supplement_dataframe = self.get_supplement_event_dataframe(self.supplement_event_queryset)

        # if we don't have any data for either or of these, just return an empty dataset
        if productivity_log_dataframe.empty or supplement_dataframe.empty:
            return pd.DataFrame()

        # axis of zero means to align them based on column
        # we want to align it based on matching index, so axis=1
        # this seems kind of weird though for axis of 1 to mean the index, shrug
        concat_df = pd.concat([supplement_dataframe, productivity_log_dataframe], axis=1)
        return concat_df
