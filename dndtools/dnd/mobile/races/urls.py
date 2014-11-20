# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.mobile.races.views',

    # races
    url(
        r'^$',
        'race_index_mobile',
        name='race_index_mobile',
    ),
    # races > by rulebooks
    url(
        r'^by-rulebooks/$',
        'race_list_by_rulebook_mobile',
        name='race_list_by_rulebook_mobile',
    ),
    # races > rulebook
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'races_in_rulebook_mobile',
        name='races_in_rulebook_mobile',
    ),
    # races > rulebook > feat
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<race_slug>[^/]+)--(?P<race_id>\d+)/$',
        'race_detail_mobile',
        name='race_detail_mobile',
    ),
    # racial types
    url(
        r'^types/$',
        'race_type_index_mobile',
        name='race_type_index_mobile'
    ),
    # race > detail
    url(
        r'^types/(?P<race_type_slug>[^/]+)/$',
        'race_type_detail_mobile',
        name='race_type_detail_mobile'
    ),
)
