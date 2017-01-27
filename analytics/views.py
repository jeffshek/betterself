from django.views.generic.base import TemplateView


class UserProductivityAnalytics(TemplateView):
    template_name = 'productivity.html'
