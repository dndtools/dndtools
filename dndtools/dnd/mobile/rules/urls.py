# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.mobile.rules.views',

    # rules
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<rule_slug>[^/]+)--(?P<rule_id>\d+)/$',
        'rule_detail_mobile',
        name='rule_detail_mobile',
    ),

)
