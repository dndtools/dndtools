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

    # feats
    (r'^feats/', include('dndtools.dnd.mobile.feat.urls')),
)