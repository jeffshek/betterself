# -*- coding: utf-8 -*-
"""
Django settings for betterself project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ

# return where ever the project starts at
ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path()

env = environ.Env()

DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Admin
    'django.contrib.admin',
    'rest_framework.authtoken',
)
THIRD_PARTY_APPS = (
    'crispy_forms',  # Form layouts
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'rest_framework',
    'django_extensions',
    'webpack_loader',
    'django_filters',
    'phonenumber_field',
    'django_celery_beat',
    'admin_honeypot',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'betterself.users',
    'supplements',
    'vendors',
    'apis',
    'apis.fitbit',
    'events',
    'analytics',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'betterself.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = []

EXCLUDE_ADMINS_USERNAMES = env('EXCLUDE_ADMIN_USERNAMES', default='admin-user')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db('DATABASE_URL', default='postgres:///betterself'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('betterself', 'templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    str(APPS_DIR.path('betterself', 'static')),
    str(APPS_DIR.path('assets')),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': str(APPS_DIR.path('webpack-stats.json')),
    }
}

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = 'username'
# Don't require emails, if a user forgets their password, tough luck.
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'optional'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'betterself.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'betterself.users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}

ADMIN_URL_NAME = env('DJANGO_ADMIN_URL', default='zzz')
ADMIN_URL = r'^{}/'.format(ADMIN_URL_NAME)

REST_FRAMEWORK = {
    # by default, someone will need to be logged in before they are
    # able to view any rest points
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/hour',
        'anon': '1000/hour',
        'signups': '10/day',
        'rescuetime-api-sync': '5/day',
        'fitbit-api-sync': '10/day',
        'demo_signups': '50/day',  # let a user create a few more demo accounts
        'user_export_all_data': '20/day',
    }
}

FITBIT_CONSUMER_KEY = env('FITBIT_CONSUMER_KEY', default='FITBIT_CONSUMER_KEY')
FITBIT_CONSUMER_SECRET = env('FITBIT_CONSUMER_SECRET', default='FITBIT_CONSUMER_SECRET')
FITBIT_LOGIN_REDIRECT = '/dashboard/logs/sleep'

TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID', default='TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN', default='TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = env('TWILIO_PHONE_NUMBER', default='16175555555')


# TODO - Reorganize all of these to be different based on staging/production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO'
        },
    },
    'loggers': {
        # assuming this gets server side errors
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # have to do this because not nesting everything under "django"
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# celery's autodiscover is slightly failing you
CELERY_IMPORTS = ['apis.rescuetime.tasks', 'apis.twilio.tasks']
