# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.races.views',

    # races
    url(
        r'^$',
        'race_index',
        name='race_index',
    ),
    # races > by rulebooks
    url(
        r'^by-rulebooks/$',
        'race_list_by_rulebook',
        name='race_list_by_rulebook',
    ),
    # races > rulebook
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'races_in_rulebook',
        name='races_in_rulebook',
    ),
    # races > rulebook > feat
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<race_slug>[^/]+)--(?P<race_id>\d+)/$',
        'race_detail',
        name='race_detail',
    ),
    # racial types
    url(
        r'^types/$',
        'race_type_index',
        name='race_type_index'
    ),
    # race > detail
    url(
        r'^types/(?P<race_type_slug>[^/]+)/$',
        'race_type_detail',
        name='race_type_detail'
    ),
)
