# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'dndtools.dnd.monsters.views',

    # monsters
    url(
        r'^$',
        'monster_index',
        name='monster_index',
    ),
    # monsters > by rulebooks
    url(
        r'^by-rulebooks/$',
        'monster_list_by_rulebook',
        name='monster_list_by_rulebook',
    ),
    # monsters > rulebook
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'monsters_in_rulebook',
        name='monsters_in_rulebook',
    ),
    # monsters > rulebook > feat
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<monster_slug>[^/]+)--(?P<monster_id>\d+)/$',
        'monster_detail',
        name='monster_detail',
    ),
)
