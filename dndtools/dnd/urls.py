# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from dndtools.dnd.feeds import AdminLogFeed


urlpatterns = patterns(
    'dndtools.dnd.views',

    (r'^robots\.txt$', direct_to_template,
     {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    # index
    url(
        r'^$',
        'index',
        name='index',
    ),
    # rulebooks
    url(
        r'^rulebooks/$',
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
        r'^rulebooks/(?P<edition_slug>[^/]+)--(?P<edition_id>\d+)/$',
        'edition_detail',
        name='edition_detail',
    ),
    # rulebooks > edition > rulebook (rulebook detail, links to spells/feats)
    url(
        r'^rulebooks/(?P<edition_slug>[^/]+)--(?P<edition_id>\d+)/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'rulebook_detail',
        name='rulebook_detail',
    ),
    # feats
    url(
        r'^feats/$',
        'feat_index',
        name='feat_index',
    ),
    # feats > by rulebooks
    url(
        r'^feats/by-rulebooks/$',
        'feat_list_by_rulebook',
        name='feat_list_by_rulebook',
    ),
    #feats > categories
    url(
        r'^feats/categories/$',
        'feat_category_list',
        name='feat_category_list',
    ),
    #feats > categories > category
    url(
        r'^feats/categories/(?P<category_slug>[^/]+)/$',
        'feat_category_detail',
        name='feat_category_detail',
    ),
    # feats > rulebook
    url(
        r'^feats/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'feats_in_rulebook',
        name='feats_in_rulebook',
    ),
    # feats > rulebook > feat
    url(
        r'^feats/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<feat_slug>[^/]+)--(?P<feat_id>\d+)/$',
        'feat_detail',
        name='feat_detail',
    ),
    # spells
    url(
        r'^spells/$',
        'spell_index',
        name='spell_index',
    ),
    # spells > by rulebooks
    url(
        r'^spells/by-rulebooks/$',
        'spell_list_by_rulebook',
        name='spell_list_by_rulebook',
    ),
    # spells > rulebook
    url(
        r'^spells/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'spells_in_rulebook',
        name='spells_in_rulebook',
    ),
    # spells > rulebook > spell
    url(
        r'^spells/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<spell_slug>[^/]+)--(?P<spell_id>\d+)/$',
        'spell_detail',
        name='spell_detail',
    ),
    # spells > descriptors
    url(
        r'^spells/descriptors/$',
        'spell_descriptor_list',
        name='spell_descriptor_list',
    ),
    # spells > descriptors > descriptor
    url(
        r'^spells/descriptors/(?P<spell_descriptor_slug>[^/]+)/$',
        'spell_descriptor_detail',
        name='spell_descriptor_detail',
    ),
    # spells > schools
    url(
        r'^spells/schools/$',
        'spell_school_list',
        name='spell_school_list',
    ),
    # spells > schools > detail
    url(
        r'^spells/schools/(?P<spell_school_slug>[^/]+)/$',
        'spell_school_detail',
        name='spell_school_detail',
    ),
    # spells > sub_schools > detail
    url(
        r'^spells/sub-schools/(?P<spell_sub_school_slug>[^/]+)/$',
        'spell_sub_school_detail',
        name='spell_sub_school_detail',
    ),
    # spells > domains
    url(
        r'^spells/domains/$',
        'spell_domain_list',
        name='spell_domain_list',
    ),
    # spells > schools > detail
    url(
        r'^spells/domains/(?P<spell_domain_slug>[^/]+)/$',
        'spell_domain_detail',
        name='spell_domain_detail',
    ),
    # classes
    url(
        r'^classes/$',
        'character_class_list',
        name='character_class_list',
    ),
    # classes > detail
    url(
        r'^classes/(?P<character_class_slug>[^/]+)/$',
        'character_class_detail',
        name='character_class_detail',
    ),
    # classes > detail
    url(
        r'^classes/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<character_class_slug>[^/]+)/$',
        'character_class_detail',
        name='character_class_variant_detail',
    ),
    # classes > detail > spells by level
    url(
        r'^classes/(?P<character_class_slug>[^/]+)/spells-level-(?P<level>\d)/$',
        'character_class_spells',
        name='character_class_spells',
    ),
    # classes > rulebook
    url(
        r'^classes/rulebook/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'character_classes_in_rulebook',
        name='character_classes_in_rulebook',
    ),
    # skills
    url(
        r'^skills/$',
        'skill_list',
        name='skill_list',
    ),
    # skills > detail
    url(
        r'^skills/(?P<skill_slug>[^/]+)/$',
        'skill_detail',
        name='skill_detail',
    ),
    # skills > detail (variant)
    url(
        r'^skills/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<skill_slug>[^/]+)/$',
        'skill_detail',
        name='skill_variant_detail',
    ),
    # skills > rulebook
    url(
        r'^skills/rulebook/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'skills_in_rulebook',
        name='skills_in_rulebook',
    ),

    # MONSTERS
    # monsters
    url(
        r'^monsters/$',
        'monster_index',
        name='monster_index',
    ),
    # monsters > by rulebooks
    url(
        r'^monsters/by-rulebooks/$',
        'monster_list_by_rulebook',
        name='monster_list_by_rulebook',
    ),
    # monsters > rulebook
    url(
        r'^monsters/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'monsters_in_rulebook',
        name='monsters_in_rulebook',
    ),
    # monsters > rulebook > feat
    url(
        r'^monsters/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<monster_slug>[^/]+)--(?P<monster_id>\d+)/$',
        'monster_detail',
        name='monster_detail',
    ),


    # races
    url(
        r'^races/$',
        'race_index',
        name='race_index',
    ),
    # races > by rulebooks
    url(
        r'^races/by-rulebooks/$',
        'race_list_by_rulebook',
        name='race_list_by_rulebook',
    ),
    # races > rulebook
    url(
        r'^races/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'races_in_rulebook',
        name='races_in_rulebook',
    ),
    # races > rulebook > feat
    url(
        r'^races/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<race_slug>[^/]+)--(?P<race_id>\d+)/$',
        'race_detail',
        name='race_detail',
    ),


    # radial types
    url(
        r'^races/types/$',
        'race_type_index',
        name='race_type_index'
    ),
    # languages > detail
    url(
        r'^races/types/(?P<race_type_slug>[^/]+)/$',
        'race_type_detail',
        name='race_type_detail'
    ),


    # ITEMS


    # items
    url(
        r'^items/$',
        'item_index',
        name='item_index',
    ),
    # items > by rulebooks
    url(
        r'^items/by-rulebooks/$',
        'item_list_by_rulebook',
        name='item_list_by_rulebook',
        ),
    # items > rulebook
    url(
        r'^items/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/$',
        'items_in_rulebook',
        name='items_in_rulebook',
        ),
    # items > rulebook > item
    url(
        r'^items/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<item_slug>[^/]+)--(?P<item_id>\d+)/$',
        'item_detail',
        name='item_detail',
    ),

    # LANGUAGES

    # languages
    url(
        r'^languages/$',
        'language_index',
        name='language_index'
    ),
    # languages > detail
    url(
        r'^languages/(?P<language_slug>[^/]+)/$',
        'language_detail',
        name='language_detail'
    ),

    # OTHERS

    # contact
    url(
        r'^contact/$',
        'contact',
        name='contact',
    ),
    # contact > sent
    url(
        r'^contact/sent/$',
        'contact_sent',
        name='contact_sent',
    ),
    # inaccurate
    url(
        r'^inaccurate_content/$',
        'inaccurate_content',
        name='inaccurate_content',
    ),
    # inaccurate > sent
    url(
        r'^inaccurate_content/sent/$',
        'inaccurate_content_sent',
        name='inaccurate_content_sent',
    ),
    # staff
    url(
        r'^staff/$',
        'staff',
        name='staff',
    ),
    (r'^rss.xml$', AdminLogFeed()),
    # rules
    url(
        r'^rules/(?P<rulebook_slug>[^/]+)--(?P<rulebook_id>\d+)/(?P<rule_slug>[^/]+)--(?P<rule_id>\d+)/$',
        'rule_detail',
        name='rule_detail',
    ),
    # job
    url(
        r'^very_secret_url/$',
        'very_secret_url',
        name='very_secret_url',
    ),

    # mobile patterns
    (r'^m/', include('dndtools.dnd.mobile.urls')),
)

# key: FUNC name, value: URL name!
desktop_to_mobile = {
    'feat_index': 'feat_index_mobile',
    'feat_list_by_rulebook': 'feat_list_by_rulebook_mobile',
    'feat_category_list': 'feat_category_list_mobile',
    'feat_category_detail': 'feat_category_detail_mobile',
    'feats_in_rulebook': 'feats_in_rulebook_mobile',
    'feat_detail': 'feat_detail_mobile',
}