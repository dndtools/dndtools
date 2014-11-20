# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.mobile.skills.views',

    # skills
    url(
        r'^$',
        'skill_list_mobile',
        name='skill_list_mobile',
    ),
    # skills > by rulebooks
    url(
        r'^by-rulebooks/$',
        'skills_list_by_rulebook_mobile',
        name='skills_list_by_rulebook_mobile',
    ),
    # skills > detail
    url(
        r'^(?P<skill_slug>[^/]+)/$',
        'skill_detail_mobile',
        name='skill_detail_mobile',
    ),
    # skills > detail (variant)
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<skill_slug>[^/]+)/$',
        'skill_detail_mobile',
        name='skill_variant_detail_mobile',
    ),
    # skills > rulebook
    url(
        r'^rulebook/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'skills_in_rulebook_mobile',
        name='skills_in_rulebook_mobile',
    ),
)
