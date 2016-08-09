from django.conf.urls import url

from apis.betterself.v1.views import SupplementView, VendorView, IngredientCompositionView
from supplements.models import IngredientComposition, Supplement
from vendors.models import Vendor

urlpatterns = [
    # urls should contain all rest resources
    url(r'^{0}'.format(Supplement.RESOURCE_NAME), SupplementView.as_view()),
    url(r'^{0}'.format(Vendor.RESOURCE_NAME), VendorView.as_view()),
    url(r'^{0}'.format(IngredientComposition.RESOURCE_NAME), IngredientCompositionView.as_view()),
]
