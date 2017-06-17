# -*- coding: utf-8 -*-
"""
This file has a REALLY stupid name because if it's just named test*.py
unittest imports this. It won't set the settings, but I rather one less thing
being imported at tests.
"""
print ('Using {} configurations'.format(__name__))

from config.settings.common import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='*v@g2i-82&uk+3jhsje_56_)9bmx_yg=o54!=1tqj*p#zf!d!m')

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
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
