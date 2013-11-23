# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'dndtools.dnd.contacts.views',

    # contact
    url(
        r'^$',
        'contact',
        name='contact',
    ),
    # contact > sent
    url(
        r'^sent/$',
        'contact_sent',
        name='contact_sent',
    ),
    # staff
    url(
        r'^staff/$',
        'staff',
        name='staff',
    ),
)
