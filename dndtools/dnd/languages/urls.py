# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'dndtools.dnd.languages.views',

    # languages
    url(
        r'^$',
        'language_index',
        name='language_index'
    ),
    # languages > detail
    url(
        r'^(?P<language_slug>[^/]+)/$',
        'language_detail',
        name='language_detail'
    ),
)
