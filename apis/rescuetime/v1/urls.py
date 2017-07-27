from django.conf.urls import url

from apis.rescuetime.v1.views import UpdateRescueTimeAPIView

urlpatterns = [
    # /api/v1/rescuetime/update-productivity-history
    url(r'^update-productivity-history$', UpdateRescueTimeAPIView.as_view(), name='rescuetime-user-update-productivity-history'),  # noqa
]
