from django.conf.urls import url

from apis.fitbit.views import FitbitLoginView, FitbitCompleteView

urlpatterns = [
    url(r'^oauth2/login/$', FitbitLoginView.as_view(), name='fitbit-login'),
    url(r'^oauth2/callback/$', FitbitCompleteView.as_view(), name='fitbit-complete'),
]
