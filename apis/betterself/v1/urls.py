from django.conf.urls import url, include

from apis.betterself.v1.events.views import SupplementEventView, ProductivityLogView, UserActivityView, \
    UserActivityEventView, ProductivityLogAggregatesView, SupplementLogListView, SupplementReminderView, \
    AggregatedSupplementLogView
from apis.betterself.v1.analytics.views import SupplementAnalyticsSummary, SupplementSleepAnalytics, \
    SupplementProductivityAnalytics, SupplementDosageAnalytics
from apis.betterself.v1.sleep.views import SleepActivityView, SleepAggregatesView, SleepAveragesView
from apis.betterself.v1.correlations.views import SleepActivitiesUserActivitiesCorrelationsView, \
    SleepActivitiesSupplementsCorrelationsView, ProductivityLogsSupplementsCorrelationsView, \
    ProductivityLogsUserActivitiesCorrelationsView
from apis.betterself.v1.signup.views import CreateUserView, CreateDemoUserView
from apis.betterself.v1.supplements.views import VendorView, IngredientCompositionView, \
    IngredientView, MeasurementView, SupplementsListView
from apis.betterself.v1.users.views import UserInfoView, UserPhoneNumberView
from apis.betterself.v1.exports.views import UserExportAllData
from events.models import SupplementLog, DailyProductivityLog, UserActivity, UserActivityLog, SleepLog, \
    SupplementReminder
from supplements.models import IngredientComposition, Supplement, Ingredient, Measurement
from vendors.models import Vendor

urlpatterns = [
    # page looks like 127.0.0.1:8001/{Supplement.RESOURCE_NAME}/
    url(r'^{0}/$'.format(Vendor.RESOURCE_NAME), VendorView.as_view(), name=Vendor.RESOURCE_NAME),
    url(r'^{0}/'.format(Supplement.RESOURCE_NAME),
            include([
                url(r'^$', SupplementsListView.as_view(), name=Supplement.RESOURCE_NAME),
                url(r'^(?P<supplement_uuid>[^/]+)/', include([
                    url(r'^log/$', SupplementLogListView.as_view(), name='supplement-log'),
                    url(r'^log/aggregate/$', AggregatedSupplementLogView.as_view(), name='aggregate-supplement-log'),
                    url(r'^analytics/summary/$', SupplementAnalyticsSummary.as_view(), name='supplement-analytics-summary'),  # noqa
                    url(r'^analytics/sleep/$', SupplementSleepAnalytics.as_view(), name='supplement-analytics-sleep'),  # noqa
                    url(r'^analytics/productivity/$', SupplementProductivityAnalytics.as_view(), name='supplement-analytics-productivity'),  # noqa
                    url(r'^analytics/dosages/$', SupplementDosageAnalytics.as_view(), name='supplement-analytics-dosages'),  # noqa
                ])),
            ])),
    url(r'^{0}/$'.format(Ingredient.RESOURCE_NAME), IngredientView.as_view(), name=Ingredient.RESOURCE_NAME),
    url(r'^{0}/$'.format(Measurement.RESOURCE_NAME), MeasurementView.as_view(), name=Measurement.RESOURCE_NAME),
    url(r'^{0}/$'.format(IngredientComposition.RESOURCE_NAME), IngredientCompositionView.as_view(),
        name=IngredientComposition.RESOURCE_NAME),
    url(r'^{0}/$'.format(SupplementLog.RESOURCE_NAME), SupplementEventView.as_view(),
        name=SupplementLog.RESOURCE_NAME),
    url(r'^{0}/'.format(DailyProductivityLog.RESOURCE_NAME),
        include([
            url(r'^$', ProductivityLogView.as_view(), name=DailyProductivityLog.RESOURCE_NAME),
            url(r'^user_activities/correlations$', ProductivityLogsUserActivitiesCorrelationsView.as_view(), name='productivity-user-activities-correlations'),  # noqa
            url(r'^supplements/correlations$', ProductivityLogsSupplementsCorrelationsView.as_view(), name='productivity-supplements-correlations'),  # noqa
            url(r'^aggregates/$', ProductivityLogAggregatesView.as_view(), name='productivity-aggregates'),  # noqa
        ])),
    url(r'^{0}/$'.format(UserActivity.RESOURCE_NAME), UserActivityView.as_view(), name=UserActivity.RESOURCE_NAME),
    url(r'^{0}/$'.format(UserActivityLog.RESOURCE_NAME), UserActivityEventView.as_view(), name=UserActivityLog.RESOURCE_NAME),  # noqa
    url(r'^{0}/'.format(SleepLog.RESOURCE_NAME),
        include([
            url(r'^$', SleepActivityView.as_view(), name=SleepLog.RESOURCE_NAME),
            url(r'^aggregates$', SleepAggregatesView.as_view(), name='sleep-aggregates'),
            url(r'^averages$', SleepAveragesView.as_view(), name='sleep-averages'),
            url(r'^user_activities/correlations$', SleepActivitiesUserActivitiesCorrelationsView.as_view(), name='sleep-user-activities-correlations'),  # noqa
            url(r'^supplements/correlations$', SleepActivitiesSupplementsCorrelationsView.as_view(), name='sleep-supplements-correlations'),  # noqa
        ])),
    url(r'^{0}/$'.format(SupplementReminder.RESOURCE_NAME), SupplementReminderView.as_view(), name=SupplementReminder.RESOURCE_NAME),  # noqa
    # The pages below are used by the front-end to create API requests that do business logic
    url(r'user-signup/$', CreateUserView.as_view(), name='api-create-user'),
    url(r'user-signup-demo/$', CreateDemoUserView.as_view(), name='api-create-demo-user'),
    url(r'user-info/$', UserInfoView.as_view(), name='api-logged-in-user-details'),
    # debate if you prefer this url structure instead of the current pattern
    url(r'user/export-data/$', UserExportAllData.as_view(), name='api-user-export-all-data'),
    url(r'user/phone_number/$', UserPhoneNumberView.as_view(), name='api-user-phone-number'),
]

API_V1_LIST_CREATE_URL = '/api/v1/{0}/'
