import pandas as pd

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from analytics.events.analytics import DataFrameEventsAnalyzer
from analytics.events.utils.dataframe_builders import AggregateDataframeBuilder


class UserProductivityAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/productivity.html'
    namespace_url_name = 'user_productivity'
    # if a user isn't logged in, redirect to exception
    redirect_field_name = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        aggregate_dataframe = AggregateDataframeBuilder.get_aggregate_dataframe_for_user(user)

        # pycharm, you so amazing, the fact that you know the dataframe's methods this many abstractions
        # is kind of like MIND BLOWING
        context['aggregate_dataframe'] = aggregate_dataframe
        context['aggregate_dataframe_html'] = aggregate_dataframe.to_html()

        if not aggregate_dataframe.empty:
            analyzer = DataFrameEventsAnalyzer(aggregate_dataframe)

            # not the prettiest, refactor to validate ahead of this
            try:
                analyzed_dataframe = analyzer.get_correlation_across_summed_days_for_measurement('Productivity')
                context['analyzed_dataframe'] = analyzed_dataframe
                context['analyzed_dataframe_html'] = analyzed_dataframe.to_html()
            except KeyError:
                # productivity columns might not exist, so skip it
                pass
        else:
            empty_df = pd.DataFrame()
            context['analyzed_dataframe'] = empty_df
            context['analyzed_dataframe_html'] = empty_df.to_html()

        return context
