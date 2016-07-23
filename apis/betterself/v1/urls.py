from apis.betterself.v1.views import APIv1Views
from django.conf.urls import url

urlpatterns = [
    # urls should contain all rest resources
    url(r'^supplements', APIv1Views.as_view()),
]
