from django.conf.urls import url

from apis.betterself.v1.views import SupplementView

urlpatterns = [
    # urls should contain all rest resources
    url(r'^supplements', SupplementView.as_view()),
]
