from django.conf.urls import include, url

# note for api urls, even though app is plural, link is singular!
# aka /api/v1, NOT /apis/v1
urlpatterns = [
    # Include all the different version APIs
    # might be over-engineering, but I can't think
    # of anytime the first version of an API didn't get changed
    url(r'^v1/', include('apis.betterself.v1.urls')),
    url(r'^v1/rescuetime/', include('apis.rescuetime.v1.urls')),
    url(r'^fitbit/', include('apis.fitbit.urls')),
    url(r'^twilio/', include('apis.twilio.urls'))
]
