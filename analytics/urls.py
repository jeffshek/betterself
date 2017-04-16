from django.conf.urls import url

from analytics.views import UserHistoricalAnalyticsView, UserRescueTimeAnalyticsView

urlpatterns = [
    url(r'^$', UserHistoricalAnalyticsView.as_view(), name=UserHistoricalAnalyticsView.namespace_url_name),
    url(r'^rescuetime/very_productive/correlations/(?P<days_back>[0-9]+)/$',
        UserRescueTimeAnalyticsView.as_view(), name=UserRescueTimeAnalyticsView.namespace_url_name),
    url(r'^rescuetime/most_productive/$', UserRescueTimeAnalyticsView.as_view(),
        name=UserRescueTimeAnalyticsView.namespace_url_name),
]
