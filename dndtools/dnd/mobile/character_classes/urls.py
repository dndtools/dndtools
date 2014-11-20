# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dnd.mobile.character_classes.views',


    # classes
    url(
        r'^$',
        'character_class_list_mobile',
        name='character_class_list_mobile',
    ),
    # classes > detail
    url(
        r'^(?P<character_class_slug>[^/]+)/$',
        'character_class_detail_mobile',
        name='character_class_detail_mobile',
    ),
    # classes > detail
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<character_class_slug>[^/]+)/$',
        'character_class_detail_mobile',
        name='character_class_variant_detail_mobile',
    ),
    # classes > detail > spells by level
    url(
        r'^(?P<character_class_slug>[^/]+)/spells-level-(?P<level>\d)/$',
        'character_class_spells_mobile',
        name='character_class_spells_mobile',
    ),
    # classes > rulebook
    url(
        r'^rulebook/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'character_classes_in_rulebook_mobile',
        name='character_classes_in_rulebook_mobile',
    ),
)
