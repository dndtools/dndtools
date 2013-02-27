# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from dndtools.dnd.sitemap import sitemaps



admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
         {'sitemaps': sitemaps}),
    (r'^', include('dndtools.dnd.urls')),
                       )

# For development server
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
         'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
        }),
                            )
