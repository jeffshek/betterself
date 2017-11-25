from django.conf.urls import url

from apis.fitbit.views import FitbitLoginView, FitbitCompleteView, FitbitUserAuthCheck, FitbitUserUpdateSleepHistory

urlpatterns = [
    url(r'^oauth2/login/$', FitbitLoginView.as_view(), name='fitbit-login'),
    url(r'^oauth2/callback/$', FitbitCompleteView.as_view(), name='fitbit-complete-backend'),
    url(r'^user-auth-check/$', FitbitUserAuthCheck.as_view(), name='fitbit-user-auth-check'),
    url(r'^update-sleep-history/$', FitbitUserUpdateSleepHistory.as_view(), name='fitbit-user-update-sleep-history'),
]
