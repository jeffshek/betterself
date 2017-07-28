from __future__ import absolute_import, unicode_literals

from config.settings.constants import PRODUCTION
from django.conf import settings

if settings.DJANGO_ENVIRONMENT == PRODUCTION:
    import celery
    import raven
    from raven.contrib.celery import register_signal, register_logger_signal

    class Celery(celery.Celery):
        def on_configure(self):
            client = raven.Client(settings.SENTRY_DSN)

            # register a custom filter to filter out duplicate logs
            register_logger_signal(client)

            # hook into the Celery error handler
            register_signal(client)
else:
    from celery import Celery

app = Celery('betterself')
app.conf.broker_url = 'redis://localhost:6379/0'

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# later versions of celery switched to json, but since we're only dealing with python, keep as pickle
app.conf.task_serializer = 'pickle'
app.conf.accept_content = ['pickle']

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print ('Debugging Task')
