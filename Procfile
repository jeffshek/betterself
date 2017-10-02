release: python manage.py migrate
web: gunicorn config.wsgi:application
worker: env > .env; env PYTHONUNBUFFERED=true honcho start -f Procfile_celery 2>&1
