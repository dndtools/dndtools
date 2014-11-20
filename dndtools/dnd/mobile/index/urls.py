# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.mobile.index.views',


    # index
    url(
        r'^$',
        'index_mobile',
        name='index_mobile',
    ),
)
