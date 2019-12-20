"""
Django settings for smiap project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import locale
import logging
import logging.config
import random
from configparser import ConfigParser
from typing import List

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.contrib.staticfiles.storage import staticfiles_storage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.config.fileConfig(os.path.join(BASE_DIR, 'logging.ini'))
LOG = logging.getLogger('SMiAP')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', ''.join(
    [random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]
))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')

# App specific settings
BRAND = os.getenv('BRAND')
LMS_URL = os.getenv('LMS_URL')
LMS_PASSWORD = os.getenv('LMS_PASSWORD')
DEPARTMENT = os.getenv('DEPARTMENT')

# Tests settings
SELENIUM_HOST = os.getenv('SELENIUM_HOST', None)
SELENIUM_PORT = os.getenv('SELENIUM_PORT', None)

ALLOWED_HOSTS: List[str] = ['*'] if not DEBUG else [
    'localhost',
    '127.0.0.1',
    '10.8.0.0/24',
    'duck.nepnep.ru',
    'vl4dmati.mati.su'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'debug_toolbar',
    'django_registration',
    'main.apps.SmiapConfig',
]

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
)

AUTHENTICATION_BACKENDS = [
    'main.authentication_backend.MyBackend',
    'django.contrib.auth.backends.ModelBackend'
]

ROOT_URLCONF = 'smiap.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'main.context_processors.app_processor',
            ],
            'environment': 'smiap.jinja2.environment',
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates', 'django')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'board.context_processors.global_settings',
                # 'django.core.context_processors.request',
                'main.context_processors.app_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'smiap.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'TEST': {
            'NAME': 'test_smiap',
        },
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'
LOCALE = os.getenv('LOCALE', 'ru_RU.UTF-8')
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
locale.setlocale(locale.LC_ALL, LOCALE)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/res/'
STATIC_ROOT = os.getenv('STATIC_ROOT')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'uploads')
FILE_UPLOAD_PERMISSIONS = 0o644
DEFAULT_IMG = staticfiles_storage.url('default.png')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    MEDIA_ROOT,
)

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'RENDER_PANELS': True
}

INTERNAL_IPS = [
    '127.0.0.1',
    '10.8.0.2',
    '10.8.0.9'
]

FIXTURE_DIRS = (
    # os.path.join(BASE_DIR, 'main', 'fixtures'),
)

HTML_MINIFY = False if DEBUG else True
AUTH_USER_MODEL = 'main.User'

# Redgreentests settings
TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

# django-registration settings
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
# Todo: Do not use CONFIG
# REGISTRATION_SALT = CONFIG.get('app', 'registration-salt')
AUTH_USER_EMAIL_UNIQUE = True

# mail settings
# Todo: Do not use CONFIG
# EMAIL_HOST = CONFIG.get('email', 'host')
# EMAIL_PORT = CONFIG.getint('email', 'port')
# EMAIL_HOST_USER = CONFIG.get('email', 'user')
# EMAIL_HOST_PASSWORD = CONFIG.get('email', 'password')
EMAIL_USE_TLS = False
# DEFAULT_FROM_EMAIL = CONFIG.get('email', 'from')
