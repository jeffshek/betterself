from betterself import celery_app


@celery_app.task(bind=True)
def import_rescuetime_user_history(self):
    return
