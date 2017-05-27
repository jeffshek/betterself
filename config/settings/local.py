# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
"""
print ('Using {} configurations'.format(__name__))

import sys

from config.settings.common import *  # noqa

try:
    from config.settings.local_secret_settings import *
except ImportError:
    # if you have a secret API settings, import them, otherwise on your merry way
    pass


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

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

# vagrants internal ip is 10.x
INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

LOCAL_DB_SETTINGS = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'betterself',
    'USER': 'vagrant',
}

# if running python manage.py test, sqlite for now
if 'test' in sys.argv:
    LOCAL_DB_SETTINGS['ENGINE'] = 'django.db.backends.sqlite3'

DATABASES['default'] = LOCAL_DB_SETTINGS

# Where API Endpoints should hit
API_ENDPOINT = 'http://127.0.0.1:9000'

# Use this to debug whitenoise issues
# Use Whitenoise to serve static files
# See: https://whitenoise.readthedocs.io/
# WHITENOISE_MIDDLEWARE = (
#     'whitenoise.middleware.WhiteNoiseMiddleware',
# )
# MIDDLEWARE_CLASSES = WHITENOISE_MIDDLEWARE + MIDDLEWARE_CLASSES
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
