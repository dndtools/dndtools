# -*- coding: utf-8 -*-
from django.db.models import Q

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from dndtools.dnd.menu import menu_item, submenu_item

from dndtools.dnd.filters import LanguageFilter
from dndtools.dnd.mobile.dnd_paginator import DndMobilePaginator
from dndtools.dnd.models import Language, Race


@menu_item("races_monsters")
@submenu_item("languages")
def language_index_mobile(request):
    f = LanguageFilter(request.GET, queryset=Language.objects.distinct())

    paginator = DndMobilePaginator(f.qs, request)

    form_submitted = 1 if '_filter' in request.GET else 0

    return render_to_response('dnd/mobile/languages/language_index.html',
                              {
                                  'request': request,
                                  'language_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item("races_monsters")
@submenu_item("languages")
def language_detail_mobile(request, language_slug):
    language = get_object_or_404(
        Language.objects, slug=language_slug,
    )
    assert isinstance(language, Language)

    race_list = Race.objects.filter(Q(automatic_languages=language) | Q(bonus_languages=language)).select_related(
        'rulebook').distinct().all()

    paginator = DndMobilePaginator(race_list, request)

    return render_to_response('dnd/mobile/languages/language_detail.html',
                              {
                                  'language': language,
                                  'paginator': paginator,
                                  'race_list': race_list,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                              }, context_instance=RequestContext(request), )