import pandas as pd
import numpy as np

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.events.utils.dataframe_builders import SupplementEventsDataframeBuilder, SleepActivityDataframeBuilder, \
    ProductivityLogEventsDataframeBuilder
from betterself.utils.api_utils import get_api_value_formatted
from constants import VERY_PRODUCTIVE_TIME_LABEL
from betterself.utils.date_utils import get_current_date_years_ago
from events.models import SupplementEvent, SleepActivity, DailyProductivityLog
from supplements.models import Supplement


class SupplementAnalyticsMixin(object):
    @staticmethod
    def _get_daily_supplement_events_series_last_year(user, supplement):
        # TODO - This may serve better as a supplement fetcher mixin
        """
        :param user:
        :param supplement:
        :return: TimeSeries data of how many of that particular supplement was taken that day
        """

        start_date = get_current_date_years_ago(1)
        supplement_events = SupplementEvent.objects.filter(user=user, supplement=supplement, time__date__gte=start_date)
        builder = SupplementEventsDataframeBuilder(supplement_events)
        series = builder.get_flat_daily_dataframe()[supplement.name]
        return series

    @staticmethod
    def _get_sleep_series_last_year(user):
        """
        :param user:
        :return: Series data of how much sleep that person has gotten minutes
        """
        start_date = get_current_date_years_ago(1)
        sleep_events = SleepActivity.objects.filter(user=user, start_time__date__gte=start_date)
        builder = SleepActivityDataframeBuilder(sleep_events)
        series = builder.get_sleep_history_series()

        # anytime sleep is actually set at zero, the value should be NaN
        series[series == 0] = np.NaN

        return series

    @staticmethod
    def _get_productivity_series_last_year(user):
        start_date = get_current_date_years_ago(1)
        logs = DailyProductivityLog.objects.filter(user=user, date__gte=start_date)
        builder = ProductivityLogEventsDataframeBuilder(logs)
        series = builder.get_flat_daily_dataframe()[VERY_PRODUCTIVE_TIME_LABEL]
        return series


class SupplementAnalyticsSummary(APIView, SupplementAnalyticsMixin):
    def get(self, request, supplement_uuid):
        user = request.user
        supplement = get_object_or_404(Supplement, uuid=supplement_uuid, user=user)
        supplement_series = self._get_daily_supplement_events_series_last_year(user, supplement)
        sleep_series = self._get_sleep_series_last_year(user)
        productivity_series = self._get_productivity_series_last_year(user)

        dataframe_details = {
            'supplement': supplement_series,
            'sleep': sleep_series,
            'productivity': productivity_series
        }

        dataframe = pd.DataFrame(dataframe_details)

        # i find a week is generally the best analysis to use for correlation, otherwise
        # you have odd days like sunday when everyone is lazy and mondays when everyone is trying
        # to do as much as possible interfering with correlations
        dataframe_rolling_week = dataframe.rolling(window=7, min_periods=1).sum()

        supplement_correlation_series = dataframe_rolling_week.corr()['supplement']

        # TODO - What should happen if any of these results are null / none?
        productivity_correlation_value = supplement_correlation_series['productivity']
        sleep_correlation_value = supplement_correlation_series['sleep']
        most_taken_value = supplement_series.max()

        # there are multi possibilities that the most caffeine was ever drank
        most_taken_dates = supplement_series[supplement_series == most_taken_value].index
        most_taken_dates = [item.isoformat() for item in most_taken_dates]

        # order by time because we don't really care about create time, rather the time the event is representing
        creation_date = SupplementEvent.objects.filter(supplement=supplement).order_by('time').first().time. \
            isoformat()

        results = [
            get_api_value_formatted(
                'productivity_correlation', productivity_correlation_value, 'Productivity Correlation'
            ),
            get_api_value_formatted(
                'sleep_correlation', sleep_correlation_value, 'Sleep Correlation'
            ),
            get_api_value_formatted(
                'most_taken', most_taken_value, 'Most Servings Taken (24 Hours)'
            ),
            get_api_value_formatted(
                'most_taken_dates', most_taken_dates, 'Most Taken Dates (24 Hours)', data_type='list-datetime'
            ),
            get_api_value_formatted(
                'creation_date', creation_date, 'Initial Record Date', data_type='string-datetime'
            ),
        ]

        return Response(results)


class SupplementSleepAnalytics(APIView, SupplementAnalyticsMixin):
    def get(self, request, supplement_uuid):
        user = request.user
        supplement = get_object_or_404(Supplement, uuid=supplement_uuid, user=user)
        supplement_series = self._get_daily_supplement_events_series_last_year(user, supplement)
        sleep_series = self._get_sleep_series_last_year(user)

        dataframe_details = {
            'supplement': supplement_series,
            'sleep': sleep_series,
        }

        results = []

        dataframe = pd.DataFrame(dataframe_details)

        index_of_supplement_taken_at_least_once = dataframe['supplement'].dropna().index

        dataframe_of_supplement_taken_at_least_once = dataframe.ix[index_of_supplement_taken_at_least_once]
        supplement_series = dataframe_of_supplement_taken_at_least_once['supplement']
        most_taken_value = supplement_series.max()

        most_taken_dates = supplement_series[supplement_series == most_taken_value].index
        most_taken_dataframe = dataframe_of_supplement_taken_at_least_once.ix[most_taken_dates]

        most_taken_sleep_mean = most_taken_dataframe['sleep'].max()
        most_taken_sleep_mean = get_api_value_formatted(
            'most_taken_sleep_mean', most_taken_sleep_mean, 'Mean Time Slept ({} Servings)'.format(
                most_taken_value))
        results.append(most_taken_sleep_mean)

        most_taken_sleep_median = most_taken_dataframe['sleep'].median()
        most_taken_sleep_median = get_api_value_formatted(
            'most_taken_sleep_median', most_taken_sleep_median, 'Median Time Slept ({} Servings)'.format(
                most_taken_value))
        results.append(most_taken_sleep_median)

        dates_where_no_supplement_taken = dataframe['supplement'].isnull()
        dataframe_of_no_supplement_taken = dataframe.ix[dates_where_no_supplement_taken]

        mean_sleep_no_supplement = dataframe_of_no_supplement_taken['sleep'].mean()
        mean_sleep_no_supplement = get_api_value_formatted(
            'mean_sleep_no_supplement', mean_sleep_no_supplement,
            'Mean Time Slept (0 Servings)')
        results.append(mean_sleep_no_supplement)

        median_sleep_of_no_supplement = dataframe_of_no_supplement_taken['sleep'].median()
        median_sleep_of_no_supplement = get_api_value_formatted(
            'median_sleep_of_no_supplement', median_sleep_of_no_supplement,
            'Median Time Slept (0 Servings)')
        results.append(median_sleep_of_no_supplement)

        median_sleep_taken_once = dataframe_of_supplement_taken_at_least_once['sleep'].median()
        median_sleep_taken_once = get_api_value_formatted(
            'median_sleep_taken_once', median_sleep_taken_once,
            'Median Time Slept (Min 1 Serving)')
        results.append(median_sleep_taken_once)

        mean_sleep_taken_once = dataframe_of_supplement_taken_at_least_once['sleep'].mean()
        mean_sleep_taken_once = get_api_value_formatted(
            'mean_sleep_taken_once', mean_sleep_taken_once,
            'Mean Time Slept (Min 1 Serving)')
        results.append(mean_sleep_taken_once)

        return Response(results)
