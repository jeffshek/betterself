from django.conf.urls import url

from apis.fitbit.views import FitbitLoginView, FitbitCompleteView, FitbitUserAuthCheck

urlpatterns = [
    url(r'^oauth2/login/$', FitbitLoginView.as_view(), name='fitbit-login'),
    url(r'^oauth2/callback/$', FitbitCompleteView.as_view(), name='fitbit-complete'),
    url(r'^user-auth-check/$', FitbitUserAuthCheck.as_view(), name='fitbit-user-auth-check'),
]
