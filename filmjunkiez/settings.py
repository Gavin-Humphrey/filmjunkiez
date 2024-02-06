"""
Django settings for filmjunkiez project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

#from ast import Import
#from email.policy import default
from email.policy import default
from pathlib import Path
import os
from decouple import config, Csv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from django.core.management.utils import get_random_secret_key

import sys
import dj_database_url
from FilmJunkiezEmailApp.backends.email_backend import EmailBackend




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = bool(int(os.environ.get('DEBUG', 0)))
DEBUG = False

CSRF_COOKIE_SECURE = True

#ALLOWED_HOSTS = ['.herokuapp.com']
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])


# Application definition
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",

    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "base.apps.BaseConfig",
    "user_follow.apps.UserFollowConfig",

    "rest_framework", 
    "corsheaders", 
]

AUTH_USER_MODEL = 'base.User'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

ROOT_URLCONF = "filmjunkiez.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ 
            BASE_DIR / "templates"
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "filmjunkiez.context_processors.website_email", #
            ],
        },
    },
]

WSGI_APPLICATION = "filmjunkiez.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DOCKERIZED = config('DOCKERIZED', default=False, cast=bool)
default_db_url = config('DEFAULT_DATABASE_URL', default='')

if DOCKERIZED:
    # Locally configured PostgreSQL for Docker development
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL', default=default_db_url)
        )
    }
    DATABASES['default']['CONN_MAX_AGE'] = 600

elif 'CI' in os.environ:
    # SQLite for tests in CircleCI
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

else:
    # Heroku PostgreSQL for deployment
    DATABASES = {
        'default': dj_database_url.config(
            default=config('HEROKU_POSTGRESQL_AQUA_URL', default=default_db_url)
        )
    }
    DATABASES['default']['CONN_MAX_AGE'] = 600


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
if 'CI' in os.environ:
    # Use Django's built-in static file serving during development
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    #STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage" 

STATIC_ROOT = str(BASE_DIR / 'staticfiles')

MEDIA_URL = "/media/"

MEDIA_ROOT = str(BASE_DIR / 'media' )

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = [
    "https://film-junkiez-be8d3d00a54d.herokuapp.com", 
    "http://localhost:8000",
    "http://127.0.0.1:8000",
 ]

CSRF_TRUSTED_ORIGINS = ["https://film-junkiez-be8d3d00a54d.herokuapp.com"] 

sentry_dsn = config('FILM_JUNKIEZ_SENTRY_DSN', default=None)

sentry_sdk.init(
    dsn=sentry_dsn,
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

LOGIN_REDIRECT_URL = '/base/thank_you.html'

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = "FilmJunkiezEmailApp.backends.email_backend.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False 
EMAIL_FROM = config('WEBSITE_EMAIL', default='backup@example.com')
EMAIL_HOST_USER = config('WEBSITE_EMAIL', default='backup@example.com')
EMAIL_HOST_PASSWORD = config('WEBSITE_EMAIL_PASSWORD', default='Backuppassword')

PASSWORD_RESET_TIMEOUT = 15000
    