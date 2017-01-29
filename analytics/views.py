from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class UserProductivityAnalytics(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/productivity.html'
    namespace_url_name = 'user_productivity'
    # if a user isn't logged in, redirect to exception
    redirect_field_name = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
