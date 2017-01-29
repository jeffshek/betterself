from django.conf.urls import url

from analytics.views import UserProductivityAnalytics


urlpatterns = [
    url(r'^$', UserProductivityAnalytics.as_view(), name=UserProductivityAnalytics.namespace_url),
]
