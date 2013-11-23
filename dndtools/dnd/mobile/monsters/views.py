# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from dndtools.dnd.menu import menu_item, submenu_item

from dndtools.dnd.filters import MonsterFilter
from dndtools.dnd.mobile.dnd_paginator import DndMobilePaginator
from dndtools.dnd.mobile.views import permanent_redirect_object_mobile
from dndtools.dnd.models import Monster, Rulebook
from dndtools.dnd.views import is_3e_edition, permanent_redirect_view


@menu_item("races_monsters")
@submenu_item("monsters")
def monster_index_mobile(request):
    f = MonsterFilter(request.GET, queryset=Monster.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').distinct())

    paginator = DndMobilePaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/mobile/monsters/monster_index.html',
                              {
                                  'request': request,
                                  'monster_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item("races_monsters")
@submenu_item("monsters_by_rulebooks")
def monster_list_by_rulebook_mobile(request):
    rulebook_list = Rulebook.objects.select_related('dnd_edition').all()

    paginator = DndMobilePaginator(rulebook_list, request)

    return render_to_response(
        'dnd/mobile/monsters/monster_list_by_rulebook.html',
                              {
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                              }, context_instance=RequestContext(request), )


@menu_item("races_monsters")
@submenu_item("monsters_by_rulebooks")
def monsters_in_rulebook_mobile(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook, pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, monsters_in_rulebook_mobile,
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    monster_list = rulebook.monster_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndMobilePaginator(monster_list, request)

    return render_to_response('dnd/mobile/monsters/monsters_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'monster_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


@menu_item("races_monsters")
@submenu_item("monsters")
def monster_detail_mobile(request, rulebook_slug, rulebook_id, monster_slug, monster_id):
    monster = get_object_or_404(
        Monster.objects.select_related('rulebook', 'rulebook__dnd_edition', 'size',
                                       'type', ),
        pk=monster_id)

    if (monster.slug != monster_slug or
                unicode(monster.rulebook.id) != rulebook_id or
                monster.rulebook.slug != rulebook_slug):
        return permanent_redirect_object_mobile(request, monster)

    assert isinstance(monster, Monster)

    monster_speeds = monster.monsterspeed_set.select_related('type', ).all()
    monster_subtypes = monster.subtypes.all()
    monster_skills = monster.skills.select_related('skill').all()
    monster_feats = monster.feats.select_related('feat', 'feat__rulebook').all()

    return render_to_response('dnd/mobile/monsters/monster_detail.html',
                              {
                                  'monster': monster,
                                  'rulebook': monster.rulebook,
                                  'request': request,
                                  'monster_speeds': monster_speeds,
                                  'monster_subtypes': monster_subtypes,
                                  'monster_skills': monster_skills,
                                  'monster_feats': monster_feats,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(monster.rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )