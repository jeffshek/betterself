from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from analytics.events.utils.dataframe_builders import AggregateDataframeBuilder


class UserProductivityAnalytics(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/productivity.html'
    namespace_url_name = 'user_productivity'
    # if a user isn't logged in, redirect to exception
    redirect_field_name = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        dataframe = AggregateDataframeBuilder.get_aggregate_dataframe_for_user(user)

        # pycharm, you so amazing, the fact that you know the dataframe's methods this many abstractions
        # is kind of like MIND BLOWING
        context['dataframe_html'] = dataframe.to_html()

        return context
