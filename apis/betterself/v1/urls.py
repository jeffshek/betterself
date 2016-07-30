from django.conf.urls import url

from apis.betterself.v1.views import SupplementListCreateView

urlpatterns = [
    # urls should contain all rest resources
    url(r'^supplements', SupplementListCreateView.as_view()),
]
