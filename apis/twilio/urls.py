from django.conf.urls import url

from apis.twilio.views import TwilioTextMessageResponse

urlpatterns = [
    url(r'^text/reply/$', TwilioTextMessageResponse.as_view(), name='twilio-text-response'),
]
