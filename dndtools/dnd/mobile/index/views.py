# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from dndtools.dnd.views import menu_item
from dndtools.dnd.models import NewsEntry


@menu_item("home")
def index_mobile(request):
    news_entries = NewsEntry.objects.filter(enabled=True).order_by('-published')[:15]

    response = render_to_response('dnd/mobile/index/index.html',
                                  {
                                      'request': request, 'newsEntries': news_entries,
                                  },
                                  context_instance=RequestContext(request), )

    if len(news_entries):
        response.set_cookie('top_news', news_entries[0].pk, 10 * 365 * 24 * 60 * 60)

    return response