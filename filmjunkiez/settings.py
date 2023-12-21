"""
Django settings for filmjunkiez project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config, Csv


import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from django.core.management.utils import get_random_secret_key

import sys


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['localhost', '127.0.0.1', f'{os.environ.get("film-junkiez")}.herokuapp.com']
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Check if running in a Docker environment
if os.environ.get("DOCKER_ENV"):
    ALLOWED_HOSTS.append('0.0.0.0')

# Heroku app domain
heroku_domain = os.environ.get("FILM_JUNKIEZ")
if heroku_domain:
    ALLOWED_HOSTS.append(f'{heroku_domain}.herokuapp.com')


# Application definition

INSTALLED_APPS = [
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

    "corsheaders.middleware.CorsMiddleware", #

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
            ],
        },
    },
]

WSGI_APPLICATION = "filmjunkiez.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DOCKERIZED = os.environ.get('DOCKERIZED', False)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME', default='Film_Junkiez_db'),
        'USER': config('DATABASE_USER', default='Film_Junkiez_User'),
        'PASSWORD': config('DATABASE_PASSWORD', default='Film_Junkiez_Password'),
        'HOST': 'db' if 'DOCKERIZED' in os.environ else 'localhost',
        'PORT': config('DJANGO_DB_PORT', default='5432'),    
    }    
}
config.debug = True

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

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')###

MEDIA_URL = "/img/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] ####

MEDIA_ROOT = BASE_DIR / "static/img"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#CORS_ALLOW_ALL_ORIGINS = True #

CORS_ALLOWED_ORIGINS = [
    "https://film-junkiez.com"   #########
]

sentry_dsn = config('FILM_JUNKIEZ_SENTRY_DSN', default=None)

sentry_sdk.init(
    dsn=sentry_dsn,
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
