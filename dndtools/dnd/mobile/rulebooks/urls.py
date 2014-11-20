# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.mobile.rulebooks.views',

    # rulebooks
    url(
        r'^$',
        'rulebook_list_mobile',
        name='rulebook_list_mobile',
    ),
    # rulebooks > editions
    url(
        r'^editions/$',
        'edition_list_mobile',
        name='edition_list_mobile',
    ),
    # rulebooks > edition (lists books in an edition)
    url(
        r'^(?P<edition_slug>[^/]+)--(?P<edition_id>\d+)/$',
        'edition_detail_mobile',
        name='edition_detail_mobile',
    ),
    # rulebooks > edition > rulebook (rulebook detail, links to spells/feats)
    url(
        r'^(?P<edition_slug>[^/]+)--(?P<edition_id>\d+)/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'rulebook_detail_mobile',
        name='rulebook_detail_mobile',
    ),
)
