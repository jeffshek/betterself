from django.views.generic.base import TemplateView


class UserProductivityAnalytics(TemplateView):
    template_name = 'analytics/productivity.html'
    namespace_url = 'user_productivity'
