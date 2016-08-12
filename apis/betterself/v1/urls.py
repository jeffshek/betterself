from django.conf.urls import url

from apis.betterself.v1.events.views import SupplementEventView
from apis.betterself.v1.supplements.views import SupplementView, VendorView, IngredientCompositionView, \
    IngredientView, MeasurementView
from events.models import SupplementEvent
from supplements.models import IngredientComposition, Supplement, Ingredient, Measurement
from vendors.models import Vendor

urlpatterns = [
    # urls should contain all rest resources
    url(r'^{0}'.format(Vendor.RESOURCE_NAME), VendorView.as_view()),
    url(r'^{0}'.format(Supplement.RESOURCE_NAME), SupplementView.as_view()),
    url(r'^{0}'.format(Ingredient.RESOURCE_NAME), IngredientView.as_view()),
    url(r'^{0}'.format(Measurement.RESOURCE_NAME), MeasurementView.as_view()),
    url(r'^{0}'.format(IngredientComposition.RESOURCE_NAME), IngredientCompositionView.as_view()),
    url(r'^{0}'.format(SupplementEvent.RESOURCE_NAME), SupplementEventView.as_view()),
]
