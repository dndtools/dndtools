# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.feats.views',


    # feats
    url(
        r'^$',
        'feat_index',
        name='feat_index',
    ),
    #feats > categories
    url(
        r'^categories/$',
        'feat_category_list',
        name='feat_category_list',
    ),
    #feats > categories > category
    url(
        r'^categories/(?P<category_slug>[^/]+)/$',
        'feat_category_detail',
        name='feat_category_detail',
    ),
    # feats > rulebook
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'feats_in_rulebook',
        name='feats_in_rulebook',
    ),
    # feats > rulebook > feat
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<feat_slug>[^/]+)--(?P<feat_id>\d+)/$',
        'feat_detail',
        name='feat_detail',
    ),
)
