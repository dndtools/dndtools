# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'dndtools.dnd.deities.views',

    # deities
    url(
        r'^$',
        'deity_list',
        name='deity_list',
    ),
    # deities > detail
    url(
        r'^(?P<deity_slug>[^/]+)/$',
        'deity_detail',
        name='deity_detail',
    ),
)
