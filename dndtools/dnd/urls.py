# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from dnd.feeds import AdminLogFeed
from dnd.sitemap import sitemaps
from dndproject import settings

urlpatterns = patterns(
    'dnd.views',

    # index
    url(
        r'^$',
        'index',
        name='index',
    ),


    # Rulebooks
    (r'^rulebooks/', include('dnd.rulebooks.urls')),

    # Feats
    (r'^feats/', include('dnd.feats.urls')),

    # Spells
    (r'^spells/', include('dnd.spells.urls')),

    # Classes
    (r'^classes/', include('dnd.character_classes.urls')),

    # Skills
    (r'^skills/', include('dnd.skills.urls')),

    # Races
    (r'^races/', include('dnd.races.urls')),

    # Monsters
    (r'^monsters/', include('dnd.monsters.urls')),

    # Items
    (r'^items/', include('dnd.items.urls')),

    # Languages
    (r'^languages/', include('dnd.languages.urls')),

    # Contacts
    (r'^contacts/', include('dnd.contacts.urls')),

    # Rules
    (r'^rules/', include('dnd.rules.urls')),

    # deities
    (r'^deities/', include('dnd.deities.urls')),

    # OTHERS

    (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

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
    (r'^rss.xml$', AdminLogFeed()),
    (r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),

    # job
    url(
        r'^very_secret_url/$',
        'very_secret_url',
        name='very_secret_url',
    ),

    # MOBILE
    (r'^m/', include('dnd.mobile.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns(
    '',

    ('^contact/$', RedirectView.as_view(url='/contacts/')),
    ('^staff/$', RedirectView.as_view(url='/contacts/staff/')),
    ('^editions/$', RedirectView.as_view(url='/rulebooks/editions/')),
    ('^feat-(?P<feat_id>\d+)-(.*)\.html$', RedirectView.as_view(url='/feats/a--1/a--%(feat_id)s/')),
)