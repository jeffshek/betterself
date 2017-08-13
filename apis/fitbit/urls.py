from django.conf.urls import url

from apis.fitbit.views import FitbitLoginView, FitbitCompleteView

urlpatterns = [
    url(r'^login/$', FitbitLoginView, name='fitbit-login'),
    url(r'^complete/$', FitbitCompleteView, name='fitbit-complete'),
]
