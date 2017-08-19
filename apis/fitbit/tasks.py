from django.contrib.auth import get_user_model

from betterself import celery_app

User = get_user_model()


@celery_app.task()
def import_user_fitbit_history_via_api(user, start_date, end_date):
    pass
