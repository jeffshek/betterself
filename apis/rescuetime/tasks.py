from betterself import celery_app


@celery_app.task()
def import_user_history_via_api():
    return
