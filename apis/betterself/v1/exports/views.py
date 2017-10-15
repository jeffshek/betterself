import io
import pandas as pd
from django.http import HttpResponse
from rest_framework.views import APIView

from analytics.events.utils.dataframe_builders import SupplementEventsDataframeBuilder, \
    ProductivityLogEventsDataframeBuilder, SleepActivityDataframeBuilder, UserActivityEventDataframeBuilder
from constants import SLEEP_MINUTES_COLUMN
from events.models import SupplementLog, SleepLog, UserActivityLog, DailyProductivityLog


class UserExportAllData(APIView):
    throttle_scope = 'user_export_all_data'

    @staticmethod
    def _write_to_workbook(writer, dataframe, worksheet_name):
        dataframe.to_excel(writer, worksheet_name)

        worksheets = writer.sheets
        worksheet = worksheets[worksheet_name]

        # Setting the column this wide looks good for dates representation
        # Freezing at 1, 1 makes being able to scroll not a burden
        worksheet.set_column('A:A', 17)
        worksheet.freeze_panes(1, 1)

    def get(self, request):
        user = request.user

        bytes_io = io.BytesIO()
        writer = pd.ExcelWriter(bytes_io, engine='xlsxwriter', options={'remove_timezone': True})

        # supplement events
        supplement_events_worksheet_name = 'SupplementEvents'
        supplement_events = SupplementLog.objects.filter(user=user)
        df_builder = SupplementEventsDataframeBuilder(supplement_events)
        supplement_events_df = df_builder.get_flat_daily_dataframe()
        self._write_to_workbook(writer, supplement_events_df, supplement_events_worksheet_name)

        # sleep events
        sleep_activities_worksheet_name = 'SleepActivities'
        sleep_activities = SleepLog.objects.filter(user=user)
        df_builder = SleepActivityDataframeBuilder(sleep_activities)
        sleep_activities_series = df_builder.get_sleep_history_series()
        self._write_to_workbook(writer, sleep_activities_series, sleep_activities_worksheet_name)

        # user activity events
        user_activity_events_sheet_name = 'UserActivityEvents'
        user_activity_events = UserActivityLog.objects.filter(user=user)
        df_builder = UserActivityEventDataframeBuilder(user_activity_events)
        user_activity_events_df = df_builder.get_flat_daily_dataframe()
        self._write_to_workbook(writer, user_activity_events_df, user_activity_events_sheet_name)

        # productivity logs
        productivity_log_sheet_name = 'DailyProductivityLog'
        productivity_log = DailyProductivityLog.objects.filter(user=user)
        df_builder = ProductivityLogEventsDataframeBuilder(productivity_log)
        # odd why this one isn't sorted the right way
        productivity_log_df = df_builder.get_flat_daily_dataframe().sort_index(ascending=True)
        self._write_to_workbook(writer, productivity_log_df, productivity_log_sheet_name)

        all_dataframes = [productivity_log_df, supplement_events_df, user_activity_events_df]
        concat_dataframe = pd.concat(all_dataframes, axis=1)

        # include sleep which is a series and not a dataframe
        cumulative_log_sheet_name = 'Aggregate Log'
        concat_dataframe[SLEEP_MINUTES_COLUMN] = sleep_activities_series
        self._write_to_workbook(writer, concat_dataframe, cumulative_log_sheet_name)

        cumulative_14_day_dataframe_sheet_name = 'Aggregate 14 Log'
        cumulative_14_day_dataframe = concat_dataframe.rolling(window=14, min_periods=1).sum()[14:]
        self._write_to_workbook(writer, cumulative_14_day_dataframe, cumulative_14_day_dataframe_sheet_name)

        cumulative_28_day_dataframe_sheet_name = 'Aggregate 28 Log'
        cumulative_28_day_dataframe = concat_dataframe.rolling(window=28, min_periods=1).sum()[28:]
        self._write_to_workbook(writer, cumulative_28_day_dataframe, cumulative_28_day_dataframe_sheet_name)

        # make sure all the output gets writen to bytes io
        writer.close()

        # http response because we are providing data and not doing any template / rendering
        response = HttpResponse(
            bytes_io.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=user_export_data.xlsx'
        return response
