# -*- coding: utf-8 -*-
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('DnDtools', 'dndtools.eu@gmail.com'),
)

MANAGERS = ADMINS
TIME_ZONE = 'Europe/Prague'
LANGUAGE_CODE = 'en-us'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
USE_I18N = False
USE_L10N = False
ADMIN_MEDIA_PREFIX = '/media/'

MIDDLEWARE_CLASSES = (
    'dnd.mobile.middleware.MobileMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'dnd.context_processors.unread_news',
    'dnd.context_processors.disable_social',
    'dnd.context_processors.is_mobile',
    'dnd.context_processors.is_admin',
    'dnd.context_processors.menu_constants',
)

ROOT_URLCONF = 'dndproject.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dnd',
    'south',
    'debug_toolbar',
    'django.contrib.sitemaps',
)

SERVER_EMAIL = 'error@dndtools.eu'
USE_TZ = False

# LOCAL PY

MEDIA_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (STATIC_DIR, )
SITE_ID = 1

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

RECAPTCHA_PUBLIC = ''
WSGI_APPLICATION = 'dndproject.wsgi.application'

from dndproject.local import *