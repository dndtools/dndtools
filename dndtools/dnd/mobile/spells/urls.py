# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'dndtools.dnd.mobile.spells.views',

    # spells
    url(
        r'^$',
        'spell_index_mobile',
        name='spell_index_mobile',
    ),
    # spells > by rulebooks
    url(
        r'^by-rulebooks/$',
        'spell_list_by_rulebook_mobile',
        name='spell_list_by_rulebook_mobile',
    ),
    # spells > rulebook
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'spells_in_rulebook_mobile',
        name='spells_in_rulebook_mobile',
    ),
    # spells > rulebook > spell
    url(
        r'^(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<spell_slug>[^/]+)--(?P<spell_id>\d+)/$',
        'spell_detail_mobile',
        name='spell_detail_mobile',
    ),
    # spells > descriptors
    url(
        r'^descriptors/$',
        'spell_descriptor_list_mobile',
        name='spell_descriptor_list_mobile',
    ),
    # spells > descriptors > descriptor
    url(
        r'^descriptors/(?P<spell_descriptor_slug>[^/]+)/$',
        'spell_descriptor_detail_mobile',
        name='spell_descriptor_detail_mobile',
    ),
    # spells > schools
    url(
        r'^schools/$',
        'spell_school_list_mobile',
        name='spell_school_list_mobile',
    ),
    # spells > schools > detail
    url(
        r'^schools/(?P<spell_school_slug>[^/]+)/$',
        'spell_school_detail_mobile',
        name='spell_school_detail_mobile',
    ),
    # spells > sub_schools > detail
    url(
        r'^sub-schools/(?P<spell_sub_school_slug>[^/]+)/$',
        'spell_sub_school_detail_mobile',
        name='spell_sub_school_detail_mobile',
    ),
    # spells > domains
    url(
        r'^domains/$',
        'spell_domain_list_mobile',
        name='spell_domain_list_mobile',
    ),
    # spells > domains > detail
    url(
        r'^domains/(?P<spell_domain_slug>[^/]+)/$',
        'spell_domain_detail_mobile',
        name='spell_domain_detail_mobile',
    ),

    # spells > domains > detail (variant)
    url(
        r'^domains/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<spell_domain_slug>[^/]+)/$',
        'spell_domain_detail_mobile',
        name='spell_variant_domain_detail_mobile',
    ),
)
