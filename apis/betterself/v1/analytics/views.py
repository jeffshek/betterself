import datetime

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
from events.models import SupplementLog, SleepLog, DailyProductivityLog
from supplements.models import Supplement


class SupplementAnalyticsMixin(object):
    @classmethod
    def _get_analytics_dataframe(cls, user, supplement_uuid):
        supplement = get_object_or_404(Supplement, uuid=supplement_uuid, user=user)
        supplement_series = cls._get_daily_supplement_events_series_last_year(user, supplement)
        sleep_series = cls._get_sleep_series_last_year(user)
        productivity_series = cls._get_productivity_series_last_year(user)

        # if either sleep or productivity are empty, create an empty series that is timezone
        # aware (hence, matching the supplement index)
        if sleep_series.empty:
            sleep_series = pd.Series(index=supplement_series.index)

        if productivity_series.empty:
            productivity_series = pd.Series(index=supplement_series.index)

        dataframe_details = {
            'supplement': supplement_series,
            'sleep': sleep_series,
            'productivity': productivity_series
        }

        dataframe = pd.DataFrame(dataframe_details)
        return dataframe

    @staticmethod
    def _get_daily_supplement_events_series_last_year(user, supplement):
        # TODO - This may serve better as a supplement fetcher mixin
        """
        :param user:
        :param supplement:
        :return: TimeSeries data of how many of that particular supplement was taken that day
        """
        start_date = get_current_date_years_ago(1)
        supplement_events = SupplementLog.objects.filter(user=user, supplement=supplement, time__date__gte=start_date)
        builder = SupplementEventsDataframeBuilder(supplement_events)
        try:
            series = builder.get_flat_daily_dataframe()[supplement.name]
        except KeyError:
            # KeyError means it doesn't exist, so create an index that can be used for everything else
            date_range_index = pd.date_range(start=start_date, end=datetime.date.today(), tz=user.pytz_timezone)
            series = pd.Series(index=date_range_index)

        return series

    @staticmethod
    def _get_sleep_series_last_year(user):
        """
        :param user:
        :return: Series data of how much sleep that person has gotten minutes
        """
        start_date = get_current_date_years_ago(1)
        sleep_events = SleepLog.objects.filter(user=user, start_time__date__gte=start_date)
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
        try:
            series = builder.get_flat_daily_dataframe()[VERY_PRODUCTIVE_TIME_LABEL]
        except KeyError:
            return pd.Series()

        return series


class SupplementAnalyticsSummary(APIView, SupplementAnalyticsMixin):
    def get(self, request, supplement_uuid):
        dataframe = self._get_analytics_dataframe(request.user, supplement_uuid)
        supplement_series = dataframe['supplement']

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
        supplement = get_object_or_404(Supplement, uuid=supplement_uuid, user=request.user)

        try:
            creation_date = SupplementLog.objects.filter(supplement=supplement).order_by('time').first().time. \
                isoformat()
        except AttributeError:
            # no creation_date found
            creation_date = None

        results = [
            get_api_value_formatted(
                'productivity_correlation', productivity_correlation_value, 'Productivity Correlation'
            ),
            get_api_value_formatted(
                'sleep_correlation', sleep_correlation_value, 'Sleep Correlation'
            ),
            get_api_value_formatted(
                'most_taken', most_taken_value, 'Most Servings Taken (1 Day)'
            ),
            get_api_value_formatted(
                'most_taken_dates', most_taken_dates, 'Most Taken Dates', data_type='list-datetime'
            ),
            get_api_value_formatted(
                'creation_date', creation_date, 'Date of First Use', data_type='string-datetime'
            ),
        ]

        return Response(results)


class SupplementSleepAnalytics(APIView, SupplementAnalyticsMixin):
    def get(self, request, supplement_uuid):
        dataframe = self._get_analytics_dataframe(request.user, supplement_uuid)
        index_of_supplement_taken_at_least_once = dataframe['supplement'].dropna().index
        dataframe_of_supplement_taken_at_least_once = dataframe.ix[index_of_supplement_taken_at_least_once]
        supplement_series = dataframe_of_supplement_taken_at_least_once['supplement']

        most_taken_value = supplement_series.max()
        most_taken_dates = supplement_series[supplement_series == most_taken_value].index
        most_taken_dataframe = dataframe_of_supplement_taken_at_least_once.ix[most_taken_dates]

        results = []

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

        return Response(results)


class SupplementProductivityAnalytics(APIView, SupplementAnalyticsMixin):
    def get(self, request, supplement_uuid):
        dataframe = self._get_analytics_dataframe(request.user, supplement_uuid)
        index_of_supplement_taken_at_least_once = dataframe['supplement'].dropna().index
        dataframe_of_supplement_taken_at_least_once = dataframe.ix[index_of_supplement_taken_at_least_once]
        dates_where_no_supplement_taken = dataframe['supplement'].isnull()
        dataframe_of_no_supplement_taken = dataframe.ix[dates_where_no_supplement_taken]

        results = []

        productivity_series_with_supplement = dataframe_of_supplement_taken_at_least_once['productivity']
        productivity_series_without_supplement = dataframe_of_no_supplement_taken['productivity']

        # no point
        if productivity_series_with_supplement.dropna().empty:
            return Response(results)

        most_productive_time_with_supplement_raw = productivity_series_with_supplement.max()
        most_productive_time_with_supplement = get_api_value_formatted(
            'most_productive_time_with_supplement', most_productive_time_with_supplement_raw,
            'Most Productive Time (Min 1 Serving)')
        results.append(most_productive_time_with_supplement)

        most_productive_date_with_supplement = productivity_series_with_supplement.idxmax()
        most_productive_date_with_supplement = get_api_value_formatted(
            'most_productive_date_with_supplement', most_productive_date_with_supplement,
            'Most Productive Date', 'string-datetime')
        results.append(most_productive_date_with_supplement)

        least_productive_time_with_supplement = productivity_series_with_supplement.min()
        least_productive_time_with_supplement = get_api_value_formatted(
            'least_productive_time_with_supplement', least_productive_time_with_supplement,
            'Least Productive Time (Min 1 Serving)')
        results.append(least_productive_time_with_supplement)

        least_productive_date_with_supplement = productivity_series_with_supplement.idxmin()
        least_productive_date_with_supplement = get_api_value_formatted(
            'least_productive_date_with_supplement', least_productive_date_with_supplement,
            'Least Productive Date', 'string-datetime')
        results.append(least_productive_date_with_supplement)

        median_productive_time_with_supplement = productivity_series_with_supplement.median()
        median_productive_time_with_supplement = get_api_value_formatted(
            'median_productive_time_with_supplement', median_productive_time_with_supplement,
            'Median Productive Time (Min 1 Serving)')
        results.append(median_productive_time_with_supplement)

        mean_productive_time_with_supplement = productivity_series_with_supplement.mean()
        mean_productive_time_with_supplement = get_api_value_formatted(
            'mean_productive_time_with_supplement', mean_productive_time_with_supplement,
            'Mean Productive Time (Min 1 Serving)')
        results.append(mean_productive_time_with_supplement)

        median_productive_time_without_supplement = productivity_series_without_supplement.median()
        median_productive_time_without_supplement = get_api_value_formatted(
            'median_productive_time_without_supplement', median_productive_time_without_supplement,
            'Median Productive Time (0 Servings)')
        results.append(median_productive_time_without_supplement)

        mean_productive_time_without_supplement = productivity_series_without_supplement.mean()
        mean_productive_time_without_supplement = get_api_value_formatted(
            'mean_productive_time_without_supplement', mean_productive_time_without_supplement,
            'Mean Productive Time (0 Servings)')
        results.append(mean_productive_time_without_supplement)

        return Response(results)


class SupplementDosageAnalytics(APIView, SupplementAnalyticsMixin):
    def get(self, request, supplement_uuid):
        dataframe = self._get_analytics_dataframe(request.user, supplement_uuid)
        index_of_supplement_taken_at_least_once = dataframe['supplement'].dropna().index
        dataframe_of_supplement_taken_at_least_once = dataframe.ix[index_of_supplement_taken_at_least_once]

        results = []

        mean_serving_size_last_365_days = dataframe['supplement'].fillna(0).mean()
        mean_serving_size_last_365_days = get_api_value_formatted(
            'mean_serving_size_last_365_days', mean_serving_size_last_365_days,
            'Mean Serving Size (All Days)')
        results.append(mean_serving_size_last_365_days)

        median_serving_size = dataframe_of_supplement_taken_at_least_once['supplement'].median()
        median_serving_size = get_api_value_formatted(
            'median_serving_size', median_serving_size,
            'Median Serving Size (Min 1 Serving)')
        results.append(median_serving_size)

        mean_serving_size = dataframe_of_supplement_taken_at_least_once['supplement'].mean()
        mean_serving_size = get_api_value_formatted(
            'mean_serving_size', mean_serving_size,
            'Mean Serving Size (Min 1 Serving)')
        results.append(mean_serving_size)

        return Response(results)
