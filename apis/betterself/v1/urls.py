from apis.betterself.v1.views import SupplementProductView
from django.conf.urls import url

urlpatterns = [
    # urls should contain all rest resources
    url(r'^supplements', SupplementProductView.as_view()),
]
