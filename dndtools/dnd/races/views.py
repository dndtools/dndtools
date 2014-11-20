# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from dnd.menu import MenuItem
from dnd.menu import menu_item, submenu_item
from dnd.dnd_paginator import DndPaginator
from dnd.filters import (   RaceFilter, RaceTypeFilter )

from dnd.models import (Rulebook, Race, RaceType )
from dnd.views import is_3e_edition, permanent_redirect_view


@menu_item(MenuItem.BESTIARY)
@submenu_item(MenuItem.Bestiary.RACES)
def race_index(request):
    f = RaceFilter(request.GET, queryset=Race.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').distinct())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if '_filter' in request.GET else 0

    return render_to_response('dnd/races/race_index.html',
                              {
                                  'request': request,
                                  'race_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.BESTIARY)
@submenu_item(MenuItem.Bestiary.RACES)
def race_list_by_rulebook(request):
    rulebook_list = Rulebook.objects.select_related('dnd_edition').all()

    paginator = DndPaginator(rulebook_list, request)

    return render_to_response('dnd/races/race_list_by_rulebook.html',
                              {
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.BESTIARY)
@submenu_item(MenuItem.Bestiary.RACES)
def races_in_rulebook(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook, pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, 'races_in_rulebook',
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    race_list = rulebook.race_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndPaginator(race_list, request)

    return render_to_response('dnd/races/races_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'race_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.BESTIARY)
@submenu_item(MenuItem.Bestiary.RACES)
def race_detail(request, rulebook_slug, rulebook_id, race_slug, race_id):
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

    return render_to_response('dnd/races/race_detail.html',
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


@menu_item(MenuItem.BESTIARY)
@submenu_item(MenuItem.Bestiary.RACE_TYPES)
def race_type_index(request):
    f = RaceTypeFilter(request.GET, queryset=RaceType.objects.distinct())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if '_filter' in request.GET else 0

    return render_to_response('dnd/races/race_type_index.html',
                              {
                                  'request': request,
                                  'race_type_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'BaseSaveType': RaceType.BaseSaveType, # enums
                                  'BaseAttackType': RaceType.BaseAttackType, # enums
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.BESTIARY)
@submenu_item(MenuItem.Bestiary.RACE_TYPES)
def race_type_detail(request, race_type_slug):
    race_type = get_object_or_404(
        RaceType.objects, slug=race_type_slug,
    )
    assert isinstance(race_type, RaceType)

    race_list = race_type.race_set.all()

    paginator = DndPaginator(race_list, request)

    return render_to_response('dnd/races/race_type_detail.html',
                              {
                                  'race_type': race_type,
                                  'paginator': paginator,
                                  'race_list': race_list,
                                  'BaseSaveType': RaceType.BaseSaveType, # enums
                                  'BaseAttackType': RaceType.BaseAttackType, # enums
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                              }, context_instance=RequestContext(request), )

