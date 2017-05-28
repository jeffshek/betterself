from django.conf.urls import url

from apis.betterself.v1.events.views import SupplementEventView, ProductivityLogView, UserActivityView, \
    UserActivityEventView
from apis.betterself.v1.supplements.views import VendorView, IngredientCompositionView, \
    IngredientView, MeasurementView, SupplementView
from events.models import SupplementEvent, DailyProductivityLog, UserActivity, UserActivityEvent
from supplements.models import IngredientComposition, Supplement, Ingredient, Measurement
from vendors.models import Vendor

urlpatterns = [
    # page looks like 127.0.0.1:8001/{Supplement.RESOURCE_NAME}/
    url(r'^{0}/$'.format(Vendor.RESOURCE_NAME), VendorView.as_view(), name=Vendor.RESOURCE_NAME),
    url(r'^{0}/$'.format(Supplement.RESOURCE_NAME), SupplementView.as_view(), name=Supplement.RESOURCE_NAME),
    url(r'^{0}/$'.format(Ingredient.RESOURCE_NAME), IngredientView.as_view(), name=Ingredient.RESOURCE_NAME),
    url(r'^{0}/$'.format(Measurement.RESOURCE_NAME), MeasurementView.as_view(), name=Measurement.RESOURCE_NAME),
    url(r'^{0}/$'.format(IngredientComposition.RESOURCE_NAME), IngredientCompositionView.as_view(),
        name=IngredientComposition.RESOURCE_NAME),
    url(r'^{0}/$'.format(SupplementEvent.RESOURCE_NAME), SupplementEventView.as_view(),
        name=SupplementEvent.RESOURCE_NAME),
    url(r'^{0}/$'.format(DailyProductivityLog.RESOURCE_NAME), ProductivityLogView.as_view(),
        name=DailyProductivityLog.RESOURCE_NAME),
    url(r'^{0}/$'.format(UserActivity.RESOURCE_NAME), UserActivityView.as_view(),
        name=UserActivity.RESOURCE_NAME),
    url(r'^{0}/$'.format(UserActivityEvent.RESOURCE_NAME), UserActivityEventView.as_view(),
        name=UserActivityEvent.RESOURCE_NAME),
]

API_V1_LIST_CREATE_URL = '/api/v1/{0}/'
