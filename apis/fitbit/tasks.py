import fitbit

from django.contrib.auth import get_user_model
from django.conf import settings
from oauthlib.oauth2 import TokenExpiredError, InvalidGrantError

from apis.fitbit.models import UserFitbit
from betterself import celery_app

User = get_user_model()


@celery_app.task()
def import_user_fitbit_history_via_api(user, start_date, end_date):
    fitbit_user = UserFitbit.objects.get(user=user)
    fitbit_api = fitbit.Fitbit(
        client_id=settings.FITBIT_CONSUMER_KEY,
        client_secret=settings.FITBIT_CONSUMER_SECRET,
        access_token=fitbit_user.access_token,
        expires_at=fitbit_user.expires_at,
        refresh_token=fitbit_user.refresh_token
    )

    # sometimes fitbit tokens are expired, so send one request just to make sure it's updated
    try:
        fitbit_api.user_profile_get(fitbit_user.fitbit_user)
    except (TokenExpiredError, InvalidGrantError):
        # if the token has expired, remove and try again.
        # TODO - Learn how to refresh tokens
        fitbit_user.delete()
        return

    api_response = fitbit_api.get_sleep(start_date)

    # if the response doesn't contain valid data, no sense to continue
    if 'sleep' not in api_response:
        return

    sleep_results = api_response['sleep']
    for result in sleep_results:
        # do import steps
        print (result)

        # use this serializer to make sure the data is valid from fitbit
        # FitbitResponseSleepActivitySerializer
