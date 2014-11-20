# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.rulebooks.views',

    # rulebooks
    url(
        r'^$',
        'rulebook_list',
        name='rulebook_list',
    ),
    # rulebooks > editions
    url(
        r'^editions/$',
        'edition_list',
        name='edition_list',
    ),
    # rulebooks > edition (lists books in an edition)
    url(
        r'^(?P<edition_slug>[^/]+)--(?P<edition_id>\d+)/$',
        'edition_detail',
        name='edition_detail',
    ),
    # rulebooks > edition > rulebook (rulebook detail, links to spells/feats)
    url(
        r'^(?P<edition_slug>[^/]+)--(?P<edition_id>\d+)/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'rulebook_detail',
        name='rulebook_detail',
    ),
)
