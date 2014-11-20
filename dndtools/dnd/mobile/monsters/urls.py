# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.mobile.monsters.views',

    # monsters
    url(
        r'^$',
        'monster_index_mobile',
        name='monster_index_mobile',
    ),
    # monsters > by rulebooks
    url(
        r'^by-rulebooks/$',
        'monster_list_by_rulebook_mobile',
        name='monster_list_by_rulebook_mobile',
    ),
    # monsters > rulebook
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'monsters_in_rulebook_mobile',
        name='monsters_in_rulebook_mobile',
    ),
    # monsters > rulebook > feat
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<monster_slug>[^/]+)--(?P<monster_id>\d+)/$',
        'monster_detail_mobile',
        name='monster_detail_mobile',
    ),
)
