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

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dndtools2-general-ci',
        'USER': 'root',
        'PASSWORD': 'root',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
    }
}

SECRET_KEY = '_ex=pd@$*e9a8*g(3n=6zv-)igez_%s2_=1wu0$#(cop5fh##c'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (STATIC_DIR, )
SITE_ID = 1

if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_PANELS = (
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


        # 'debug_toolbar.panels.version.VersionDebugPanel',
        # 'debug_toolbar.panels.timer.TimerDebugPanel',
        # 'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        # 'debug_toolbar.panels.headers.HeaderDebugPanel',
        # 'debug_toolbar.panels.profiling.ProfilingDebugPanel',
        # 'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        # 'debug_toolbar.panels.sql.SQLDebugPanel',
        # 'debug_toolbar.panels.template.TemplateDebugPanel',
        # 'debug_toolbar.panels.cache.CacheDebugPanel',
        # 'debug_toolbar.panels.signals.SignalDebugPanel',
        # 'debug_toolbar.panels.logger.LoggingPanel',
    )

    # DEBUG_TOOLBAR_CONFIG = {
    #     'DISABLE_PANELS': False,
    # }

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

RECAPTCHA_PUBLIC = ''
WSGI_APPLICATION = 'dndproject.wsgi.application'
