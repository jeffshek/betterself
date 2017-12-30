# -*- coding: utf-8 -*-
"""
This file has a REALLY stupid name because if it's just named test*.py
unittest imports this. It won't set the settings, but I rather one less thing
being imported at tests.
"""
print ('Using {} configurations'.format(__name__))

from config.settings.common import *  # noqa
from config.settings.constants import TESTING

DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
DJANGO_ENVIRONMENT = TESTING

SECRET_KEY = env('DJANGO_SECRET_KEY', default='*v@g2i-82&uk+3jhsje_56_)9bmx_yg=o54!=1tqj*p#zf!d!m')

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

INTERNAL_IPS = ('127.0.0.1', )

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[
    'testserver']
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

TEST_DB_SETTINGS = {
    # diagnose if this is a recent change in travis breaking
    # need to probably switch this back to postgres, but travis config is a pain
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'travis_ci_test',
    'USER': 'postgres',
    'PASSWORD': '',
    'HOST': 'localhost',
}

DATABASES['default'] = TEST_DB_SETTINGS

# Where API Endpoints should hit
API_ENDPOINT = 'http://localhost:8081'

# don't check for throttling when testing
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['signups'] = '500/sec'
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['demo_signups'] = '500/sec'

# we don't want to see a large amount of spam from INFOs during testing - only show for ERRORS
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR'
        },
    },
    'loggers': {
        # assuming this gets server side errors
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        # have to do this because not nesting everything under "django"
        '': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
}

# now celery tasks autorun -- so ... write unit tests for your celery tasks.
# TODO - Do this and do it well
# CELERY_TASK_ALWAYS_EAGER = True

# run testing in parallel - you'll find out this breaks a few things
MIGRATION_MODULES = {
    # 'auth': None,
    # 'contenttypes': None,
    'default': None,
    'sessions': None,
    'core': None,
    'profiles': None,
    'snippets': None,
    'scaffold_templates': None,
    # 'users': None,
    'django_celery_beat': None,
    # 'events': None,
    'fitbit': None,
    'account': None,
    'admin': None,
    'admin_honeypot': None,
    # 'apis': None,
    'authtoken': None,
    # 'supplements': None,
    # 'vendors': None,
    'sites': None,
    'socialaccount': None,
}

# Uncomment these to see what tests are slow!
# TEST_RUNNER = 'django_slowtests.testrunner.DiscoverSlowestTestsRunner'
# NUM_SLOW_TESTS = 10
