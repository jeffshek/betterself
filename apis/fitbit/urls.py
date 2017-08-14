from django.conf.urls import url

from apis.fitbit.views import FitbitLoginView, FitbitCompleteView

urlpatterns = [
    url(r'^login/$', FitbitLoginView.as_view(), name='fitbit-login'),
    url(r'^complete/$', FitbitCompleteView.as_view(), name='fitbit-complete'),
]
