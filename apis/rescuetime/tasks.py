from django.contrib.auth import get_user_model

from apis.rescuetime.importers.historical_daily_importer import RescueTimeHistoricalDailyImporter
from betterself import celery_app

User = get_user_model()


@celery_app.task()
def import_user_history_via_api(user, start_date, end_date, rescuetime_api_key):
    importer = RescueTimeHistoricalDailyImporter(user, rescuetime_api_key)
    importer.import_history(start_date, end_date)
    importer.save()
