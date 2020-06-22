"""
Django settings for smiap project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import locale
import os
import random

from django.contrib.staticfiles.storage import staticfiles_storage

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', ''.join(
    [random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]
))


# Tests settings
SELENIUM_HOST = os.getenv('SELENIUM_HOST', None)
SELENIUM_PORT = os.getenv('SELENIUM_PORT', None)

# Configuration for django editor widgets
from djangoeditorwidgets.config import *

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
    'django_filters',
    'rest_framework',
    'sass_processor',
    'compressor',
    'colorfield',
    'djangoeditorwidgets',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'main.apps.SmiapConfig',
    'schedule.apps.ScheduleConfig',
    'news.apps.NewsConfig',
    'api.apps.ApiConfig',
    'api.v1.apps.ApiV1Config',
]

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
)

AUTHENTICATION_BACKENDS = [
    'main.authentication_backend.MyBackend',
    'django.contrib.auth.backends.ModelBackend'
]

ROOT_URLCONF = 'smiap.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [TEMPLATE_DIR],
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
        'DIRS': [os.path.join(TEMPLATE_DIR, 'django')],
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

FILES_ROOT = os.getenv('FILES_ROOT')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(FILES_ROOT, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(FILES_ROOT, 'media')
FILE_UPLOAD_PERMISSIONS = 0o644
DEFAULT_IMG = staticfiles_storage.url('default.png')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    MEDIA_ROOT,
)

INTERNAL_IPS = [
    '127.0.0.1',
    '10.8.0.2',
    '10.8.0.9'
]

FIXTURE_DIRS = (
    # os.path.join(BASE_DIR, 'main', 'fixtures'),
)

AUTH_USER_MODEL = 'main.User'

# Redgreentests settings
TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

# REST Framework config
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
    'compressor.finders.CompressorFinder',
]
