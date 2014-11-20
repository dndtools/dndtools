# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.mobile.items.views',

    # items
    url(
        r'^$',
        'item_index_mobile',
        name='item_index_mobile',
    ),
    # items > by rulebooks
    url(
        r'^by-rulebooks/$',
        'item_list_by_rulebook_mobile',
        name='item_list_by_rulebook_mobile',
    ),
    # items > rulebook
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'items_in_rulebook_mobile',
        name='items_in_rulebook_mobile',
    ),
    # items > rulebook > item
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<item_slug>[^/]+)--(?P<item_id>\d+)/$',
        'item_detail_mobile',
        name='item_detail_mobile',
    ),
)
