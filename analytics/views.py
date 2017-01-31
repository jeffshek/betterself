from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from analytics.events.utils.dataframe_builders import AggregateDataframeBuilder
from events.models import SupplementEvent, DailyProductivityLog


class UserProductivityAnalytics(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/productivity.html'
    namespace_url_name = 'user_productivity'
    # if a user isn't logged in, redirect to exception
    redirect_field_name = 'account_login'

    def _get_dataframe_raw_data(self, user):
        supplement_events = SupplementEvent.objects.filter(user=user)
        productivity_log = DailyProductivityLog.objects.filter(user=user)

        aggregate_dataframe = AggregateDataframeBuilder(
            supplement_event_queryset=supplement_events,
            productivity_log_queryset=productivity_log,
        )

        dataframe = aggregate_dataframe.build_dataframe()

        return dataframe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        dataframe = self._get_dataframe_raw_data(user)
        context['dataframe'] = dataframe

        return context
