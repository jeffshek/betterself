from django.conf.urls import url

from apis.rescuetime.v1.views import UpdateRescueTimeAPIView

urlpatterns = [
    # page looks like 127.0.0.1:8001/{Supplement.RESOURCE_NAME}/
    url(r'^rescuetime/user-api-historical-update$', UpdateRescueTimeAPIView.as_view(), name='rescuetime-user-api-update'),  # noqa
]
