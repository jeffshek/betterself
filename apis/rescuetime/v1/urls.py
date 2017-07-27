from django.conf.urls import url

from apis.rescuetime.v1.views import UpdateRescueTimeAPIView

urlpatterns = [
    # page looks like 127.0.0.1:8001/{Supplement.RESOURCE_NAME}/
    url(r'^rescuetime/update-productivity-history$', UpdateRescueTimeAPIView.as_view(), name='rescuetime-user-update-productivity-history'),  # noqa
]
