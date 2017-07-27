from betterself import celery_app


@celery_app.task(bind=True)
def import_user_history_via_api(self):
    return
