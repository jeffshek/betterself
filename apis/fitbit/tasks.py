import logging
import fitbit
import pandas as pd

from django.conf import settings
from django.contrib.auth import get_user_model

from apis.fitbit.models import UserFitbit
from apis.fitbit.serializers import FitbitResponseSleepActivitySerializer
from betterself import celery_app

logger = logging.getLogger(__name__)

User = get_user_model()


@celery_app.task()
def import_user_fitbit_history_via_api(user, start_date, end_date):
    fitbit_user = UserFitbit.objects.get(user=user)
    fitbit_api = fitbit.Fitbit(
        client_id=settings.FITBIT_CONSUMER_KEY,
        client_secret=settings.FITBIT_CONSUMER_SECRET,
        access_token=fitbit_user.access_token,
        expires_at=fitbit_user.expires_at,
        refresh_token=fitbit_user.refresh_token,
        refresh_cb=fitbit_user.refresh_cb,
    )

    query_dates = pd.date_range(start=start_date, end=end_date).date
    for query_date in query_dates:
        api_response = fitbit_api.get_sleep(query_date)

        valid_data = api_response.get('sleep')
        if not valid_data:
            # if the response doesn't contain valid data, no sense to continue
            continue

        for datum in valid_data:
            data = {
                'user': user.id,
                'start_time': datum['startTime'],
                'end_time': datum['endTime']
            }

            serializer = FitbitResponseSleepActivitySerializer(data=data)
            serializer.is_valid()
            serializer.save()
