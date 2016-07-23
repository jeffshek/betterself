from django.conf.urls import include, url

urlpatterns = [
    # Include all the different version APIs
    # might be over-engineering, but I can't think
    # of anytime the first version of an API didn't get changed
    url(r'^v1/', include('apis.betterself.v1.urls')),
]
