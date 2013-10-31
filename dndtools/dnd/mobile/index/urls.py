# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'dndtools.dnd.mobile.index.views',


    # index
    url(
        r'^$',
        'index_mobile',
        name='index_mobile',
    ),
)
