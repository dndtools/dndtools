# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'dndtools.dnd.items.views',

    # items
    url(
        r'^$',
        'item_index',
        name='item_index',
    ),
    # items > by rulebooks
    url(
        r'^by-rulebooks/$',
        'item_list_by_rulebook',
        name='item_list_by_rulebook',
    ),
    # items > rulebook
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'items_in_rulebook',
        name='items_in_rulebook',
    ),
    # items > rulebook > item
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<item_slug>[^/]+)--(?P<item_id>\d+)/$',
        'item_detail',
        name='item_detail',
    ),
)
