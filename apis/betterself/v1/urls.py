from django.conf.urls import url

from apis.betterself.v1.views import SupplementView, VendorView

urlpatterns = [
    # urls should contain all rest resources
    url(r'^supplements', SupplementView.as_view()),
    url(r'^vendors', VendorView.as_view()),
]
