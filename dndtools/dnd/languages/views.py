# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from dnd.menu import menu_item, submenu_item, MenuItem
from dnd.dnd_paginator import DndPaginator
from dnd.filters import LanguageFilter
from dnd.models import Race, Language


@menu_item(MenuItem.CHARACTER_OPTIONS)
@submenu_item(MenuItem.CharacterOptions.LANGUAGES)
def language_index(request):
    f = LanguageFilter(request.GET, queryset=Language.objects.distinct())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if '_filter' in request.GET else 0

    return render_to_response('dnd/languages/language_index.html',
                              {
                                  'request': request,
                                  'language_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.CHARACTER_OPTIONS)
@submenu_item(MenuItem.CharacterOptions.LANGUAGES)
def language_detail(request, language_slug):
    language = get_object_or_404(
        Language.objects, slug=language_slug,
    )
    assert isinstance(language, Language)

    race_list = Race.objects.filter(Q(automatic_languages=language) | Q(bonus_languages=language)).select_related(
        'rulebook').distinct().all()

    paginator = DndPaginator(race_list, request)

    return render_to_response('dnd/languages/language_detail.html',
                              {
                                  'language': language,
                                  'paginator': paginator,
                                  'race_list': race_list,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                              }, context_instance=RequestContext(request), )
