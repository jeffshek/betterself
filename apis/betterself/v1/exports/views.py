import io
import pandas as pd
from django.http import HttpResponse
from rest_framework.views import APIView

from analytics.events.utils.dataframe_builders import SupplementEventsDataframeBuilder, \
    ProductivityLogEventsDataframeBuilder, SleepActivityDataframeBuilder, UserActivityEventDataframeBuilder
from events.models import SupplementEvent, SleepActivity, UserActivityEvent, DailyProductivityLog


class UserExportAllData(APIView):
    throttle_scope = 'user_export_all_data'

    def get(self, request):
        user = request.user

        bytes_io = io.BytesIO()
        workbook = pd.ExcelWriter(bytes_io, engine='xlsxwriter', options={'remove_timezone': True})

        # supplement events
        supplement_events = SupplementEvent.objects.filter(user=user)
        df_builder = SupplementEventsDataframeBuilder(supplement_events)
        supplement_events_df = df_builder.get_flat_daily_dataframe()
        supplement_events_df.to_excel(workbook, 'SupplementEvents')

        # sleep events
        sleep_activities = SleepActivity.objects.filter(user=user)
        df_builder = SleepActivityDataframeBuilder(sleep_activities)
        sleep_activities_series = df_builder.get_sleep_history_series()
        sleep_activities_series.to_excel(workbook, 'SleepActivities')

        # user activity events
        user_activity_events = UserActivityEvent.objects.filter(user=user)
        df_builder = UserActivityEventDataframeBuilder(user_activity_events)
        user_activity_events_df = df_builder.get_flat_daily_dataframe()
        user_activity_events_df.to_excel(workbook, 'UserActivityEvents')

        # productivity logs
        productivity_log = DailyProductivityLog.objects.filter(user=user)
        df_builder = ProductivityLogEventsDataframeBuilder(productivity_log)
        # odd why this one isn't sorted the right way
        productivity_log_df = df_builder.get_flat_daily_dataframe().sort_index(ascending=True)
        productivity_log_df.to_excel(workbook, 'DailyProductivityLog')

        all_dataframes = [supplement_events_df, user_activity_events_df, productivity_log_df]

        concat_dataframe = pd.concat(all_dataframes, axis=1)
        # include sleep which is a series and not a dataframe
        concat_dataframe['Sleep Minutes'] = sleep_activities_series
        concat_dataframe.to_excel(workbook, 'Cumulative Log')

        cumulative_14_day_dataframe = concat_dataframe.fillna(0).rolling(window=14).sum()[14:]
        cumulative_14_day_dataframe.to_excel(workbook, 'Aggregate 14 Log')

        cumulative_28_day_dataframe = concat_dataframe.fillna(0).rolling(window=28).sum()[28:]
        cumulative_28_day_dataframe.to_excel(workbook, 'Aggregate 28 Log')

        # make sure all the output gets writen to bytes io
        workbook.close()

        # TODO - Find a switch way to do a DRF response
        response = HttpResponse(
            bytes_io.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=user_export_data.xlsx'
        return response
