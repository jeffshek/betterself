from django.conf.urls import url

from analytics.views import UserProductivityAnalyticsView


urlpatterns = [
    url(r'^$', UserProductivityAnalyticsView.as_view(), name=UserProductivityAnalyticsView.namespace_url_name),
]
