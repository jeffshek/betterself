from django.conf.urls import url

from apis.betterself.v1.events.views import SupplementEventView, ProductivityLogView, UserActivityView, \
    UserActivityEventView, SleepActivityView
from apis.betterself.v1.signup.views import CreateUserView, CreateDemoUserView
from apis.betterself.v1.supplements.views import VendorView, IngredientCompositionView, \
    IngredientView, MeasurementView, SupplementView
from apis.betterself.v1.users.views import UserInfoView
from events.models import SupplementEvent, DailyProductivityLog, UserActivity, UserActivityEvent, SleepActivity
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
    url(r'^{0}/$'.format(SleepActivity.RESOURCE_NAME), SleepActivityView.as_view(),
        name=SleepActivity.RESOURCE_NAME),
    # The pages below are used by the front-end to create API requests that do business logic
    url(r'user-signup/$', CreateUserView.as_view(), name='api-create-user'),
    url(r'user-signup-demo/$', CreateDemoUserView.as_view(), name='api-create-demo-user'),
    url(r'user-info/$', UserInfoView.as_view(), name='api-logged-in-user-details')
]

API_V1_LIST_CREATE_URL = '/api/v1/{0}/'
