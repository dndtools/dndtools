# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    'dnd.mobile.views',

    # force desktop
    url(
        r'^force-desktop-version/$',
        'force_desktop_version',
        name='force_desktop_version',
    ),

    # return to mobile version
    url(
        r'^return-to-mobile-version/$',
        'return_to_mobile_version',
        name='return_to_mobile_version',
    ),

    # index
    (r'^', include('dnd.mobile.index.urls')),

    # character classes
    (r'^classes/', include('dnd.mobile.character_classes.urls')),

    # feats
    (r'^feats/', include('dnd.mobile.feats.urls')),

    # items
    (r'^items/', include('dnd.mobile.items.urls')),

    # languages
    (r'^languages/', include('dnd.mobile.languages.urls')),

    # monsters
    (r'^monsters/', include('dnd.mobile.monsters.urls')),

    # races
    (r'^races/', include('dnd.mobile.races.urls')),

    # rulebooks
    (r'^rulebooks/', include('dnd.mobile.rulebooks.urls')),

    # rules
    (r'^rules/', include('dnd.mobile.rules.urls')),

    # skills
    (r'^skills/', include('dnd.mobile.skills.urls')),

    # spells
    (r'^spells/', include('dnd.mobile.spells.urls')),

    # deities
    (r'^deities/', include('dnd.mobile.deities.urls')),
)