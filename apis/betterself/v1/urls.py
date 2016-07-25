from django.conf.urls import url

from apis.betterself.v1.views import SupplementListView

urlpatterns = [
    # urls should contain all rest resources
    url(r'^supplements', SupplementListView.as_view()),
]
