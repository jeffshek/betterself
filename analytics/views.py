import pandas as pd

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from analytics.events.analytics import DataFrameEventsAnalyzer
from analytics.events.utils.dataframe_builders import AggregateSupplementProductivityDataframeBuilder


class UserHistoricalAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/history.html'
    namespace_url_name = 'user_events_history'

    # if a user isn't logged in, redirect to exception
    redirect_field_name = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        aggregate_dataframe = AggregateSupplementProductivityDataframeBuilder.get_aggregate_dataframe_for_user(user)

        context['aggregate_dataframe'] = aggregate_dataframe
        context['aggregate_dataframe_html'] = aggregate_dataframe.to_html()

        return context


class UserRescueTimeAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/rescuetime_dataframe.html'
    namespace_url_name = 'rescuetime_analytics_overview'
    # if a user isn't logged in, redirect to exception
    redirect_field_name = 'account_login'

    def get_context_data(self, days_back=0, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # comes as a string from the interwebs
        days_back = int(days_back)

        aggregate_dataframe = AggregateSupplementProductivityDataframeBuilder.get_aggregate_dataframe_for_user(user)

        # default of zero means get full history, otherwise an amount of days back lets a user
        # make more intelligence decisions about what effects and when ... some functionality
        # that makes sense might be start_date and end_date ... instead of days back
        if days_back:
            aggregate_dataframe = aggregate_dataframe[-1 * days_back:]

        if not aggregate_dataframe.empty:
            analyzer = DataFrameEventsAnalyzer(aggregate_dataframe)

            # not the prettiest, refactor to validate ahead of this
            analyzed_series = analyzer.get_correlation_across_summed_days_for_measurement(
                'Very Productive Minutes')
            analyzed_dataframe = analyzed_series.to_frame()
        else:
            # otherwise, just return an empty dataframe
            analyzed_dataframe = pd.DataFrame()

        context['dataframe'] = analyzed_dataframe
        context['dataframe_html'] = analyzed_dataframe.to_html()

        return context


class UserRescueTimeMostProductiveDaysView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/rescuetime_dataframe.html'
    namespace_url_name = 'rescuetime_best_days_dataframe'
    # if a user isn't logged in, redirect to exception
    redirect_field_name = 'account_login'

    def get_context_data(self, **kwargs):
        """
        TODO - This needs a little bit more thought as to how one should
        filter (by how many days) and how does one include previous supplements
        from the night before to add as a useful metric.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        aggregate_dataframe = AggregateSupplementProductivityDataframeBuilder.get_aggregate_dataframe_for_user(user)
        productive_days = aggregate_dataframe['Very Productive Minutes'].copy().dropna()
        productive_days = productive_days[productive_days > 1]  # don't want zero days either

        # sort them by the most productive
        productive_days.sort(ascending=False)

        # just get the top 30 most productive days
        productive_days = productive_days[0:30]

        aggregate_dataframe = aggregate_dataframe.ix[productive_days.ix]

        context['dataframe'] = aggregate_dataframe
        context['dataframe_html'] = aggregate_dataframe.to_html()

        return context
