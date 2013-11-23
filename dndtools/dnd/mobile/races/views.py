# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from dndtools.dnd.menu import menu_item, submenu_item
from dndtools.dnd.filters import RaceTypeFilter, RaceFilter
from dndtools.dnd.mobile.dnd_paginator import DndMobilePaginator
from dndtools.dnd.models import Rulebook, Race, RaceType
from dndtools.dnd.views import permanent_redirect_view, is_3e_edition


@menu_item("races_monsters")
@submenu_item("races")
def race_index_mobile(request):
    f = RaceFilter(request.GET, queryset=Race.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').distinct())

    paginator = DndMobilePaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/mobile/races/race_index.html',
                              {
                                  'request': request,
                                  'race_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item("races_monsters")
@submenu_item("races_by_rulebooks")
def race_list_by_rulebook_mobile(request):
    rulebook_list = Rulebook.objects.select_related('dnd_edition').all()

    paginator = DndMobilePaginator(rulebook_list, request)

    return render_to_response('dnd/mobile/races/race_list_by_rulebook.html',
                              {
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                              }, context_instance=RequestContext(request), )


@menu_item("races_monsters")
@submenu_item("races_by_rulebooks")
def races_in_rulebook_mobile(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook, pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, races_in_rulebook_mobile,
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    race_list = rulebook.race_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndMobilePaginator(race_list, request)

    return render_to_response('dnd/mobile/races/races_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'race_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


@menu_item("races_monsters")
@submenu_item("races")
def race_detail_mobile(request, rulebook_slug, rulebook_id, race_slug, race_id):
    race = get_object_or_404(
        Race.objects.select_related('rulebook', 'rulebook__dnd_edition', 'size', 'automatic_languages',
                                    'bonus_languages', 'race_type'),
        pk=race_id)
    assert isinstance(race, Race)

    if (race.slug != race_slug or
                unicode(race.rulebook.id) != rulebook_id or
                race.rulebook.slug != rulebook_slug):
        return permanent_redirect_view(request, 'race_detail',
                                       kwargs={
                                           'rulebook_slug': race.rulebook.slug,
                                           'rulebook_id': race.rulebook.id,
                                           'race_slug': race.slug,
                                           'race_id': race.id, })

    race_speeds = race.racespeed_set.select_related('type', ).all()
    favored_classes = race.favored_classes.select_related('character_class', ).all()

    related_races = Race.objects.filter(slug=race.slug).exclude(rulebook__id=race.rulebook.id).select_related(
        'rulebook', 'rulebook__dnd_edition').all()

    return render_to_response('dnd/mobile/races/race_detail.html',
                              {
                                  'race': race,
                                  'rulebook': race.rulebook,
                                  'request': request,
                                  'race_speeds': race_speeds,
                                  'favored_classes': favored_classes,
                                  'automatic_languages': race.automatic_languages.all(),
                                  'bonus_languages': race.bonus_languages.all(),
                                  'related_races': related_races,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(race.rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


@menu_item("races_monsters")
@submenu_item("race_types")
def race_type_index_mobile(request):
    f = RaceTypeFilter(request.GET, queryset=RaceType.objects.distinct())

    paginator = DndMobilePaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/mobile/races/race_type_index.html',
                              {
                                  'request': request,
                                  'race_type_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'BaseSaveType': RaceType.BaseSaveType, # enums
                                  'BaseAttackType': RaceType.BaseAttackType, # enums
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item("races_monsters")
@submenu_item("race_types")
def race_type_detail_mobile(request, race_type_slug):
    race_type = get_object_or_404(
        RaceType.objects, slug=race_type_slug,
    )
    assert isinstance(race_type, RaceType)

    race_list = race_type.race_set.all()

    paginator = DndMobilePaginator(race_list, request)

    return render_to_response('dnd/mobile/races/race_type_detail.html',
                              {
                                  'race_type': race_type,
                                  'paginator': paginator,
                                  'race_list': race_list,
                                  'BaseSaveType': RaceType.BaseSaveType, # enums
                                  'BaseAttackType': RaceType.BaseAttackType, # enums
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                              }, context_instance=RequestContext(request), )