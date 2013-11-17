# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns(
    'dndtools.dnd.mobile.views',

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
    (r'^', include('dndtools.dnd.mobile.index.urls')),

    # character classes
    (r'^classes/', include('dndtools.dnd.mobile.character_classes.urls')),

    # feats
    (r'^feats/', include('dndtools.dnd.mobile.feats.urls')),

    # items
    (r'^items/', include('dndtools.dnd.mobile.items.urls')),

    # languages
    (r'^languages/', include('dndtools.dnd.mobile.languages.urls')),

    # monsters
    (r'^monsters/', include('dndtools.dnd.mobile.monsters.urls')),

    # races
    (r'^races/', include('dndtools.dnd.mobile.races.urls')),

    # rulebooks
    (r'^rulebooks/', include('dndtools.dnd.mobile.rulebooks.urls')),

    # rules
    (r'^rules/', include('dndtools.dnd.mobile.rules.urls')),

    # skills
    (r'^skills/', include('dndtools.dnd.mobile.skills.urls')),

    # spells
    (r'^spells/', include('dndtools.dnd.mobile.spells.urls')),

    # deities
    (r'^deities/', include('dndtools.dnd.mobile.deities.urls')),
)