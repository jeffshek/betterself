from django.conf.urls import url

from apis.fitbit.views import FitBitLoginView

urlpatterns = [
    url(r'^fitbit/login$', FitBitLoginView, 'betterself-fitbit-login'),
]
