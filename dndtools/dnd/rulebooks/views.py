# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from dndtools.dnd.filters import RulebookFilter
from dndtools.dnd.menu import menu_item, submenu_item, MenuItem
from dndtools.dnd.dnd_paginator import DndPaginator
from dndtools.dnd.models import Rulebook, DndEdition
from dndtools.dnd.views import is_3e_edition, permanent_redirect_object


@menu_item(MenuItem.RULEBOOKS)
@submenu_item(MenuItem.Rulebooks.RULEBOOKS)
def rulebook_list(request):
    f = RulebookFilter(request.GET, queryset=Rulebook.objects.select_related(
        'dnd_edition'))

    form_submitted = 1 if 'name' in request.GET else 0

    paginator = DndPaginator(f.qs, request)

    return render_to_response('dnd/rulebooks/rulebook_list.html',
                              {
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )

@menu_item(MenuItem.RULEBOOKS)
@submenu_item(MenuItem.Rulebooks.EDITIONS)
def edition_list(request):
    edition_list = DndEdition.objects.all()

    paginator = DndPaginator(edition_list, request)

    return render_to_response('dnd/rulebooks/edition_list.html',
                              {
                                  'edition_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.RULEBOOKS)
@submenu_item(MenuItem.Rulebooks.EDITIONS)
def edition_detail(request, edition_slug, edition_id):
    dnd_edition = get_object_or_404(DndEdition, id=edition_id)
    if dnd_edition.slug != edition_slug:
        return permanent_redirect_object(request, dnd_edition)

    rulebook_list = dnd_edition.rulebook_set.select_related('dnd_edition').all()

    paginator = DndPaginator(rulebook_list, request)

    if is_3e_edition(dnd_edition):
        request.submenu_item = MenuItem.Rulebooks.BOOKS_3_0
    elif dnd_edition.slug == "core-35":
        request.submenu_item = MenuItem.Rulebooks.CORE_3_5
    elif dnd_edition.slug == "supplementals-35":
        request.submenu_item = MenuItem.Rulebooks.SUPPLEMENTS_3_5
    elif dnd_edition.slug == "dragonlance":
        request.submenu_item = MenuItem.Rulebooks.DRAGONLANCE_3_5
    elif dnd_edition.slug == "eberron-35":
        request.submenu_item = MenuItem.Rulebooks.EBERRON_3_5
    elif dnd_edition.slug == "forgotten-realms-35":
        request.submenu_item = MenuItem.Rulebooks.FORGOTTEN_REALMS_3_5

    return render_to_response('dnd/rulebooks/edition_detail.html',
                              {
                                  'dnd_edition': dnd_edition,
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(dnd_edition),
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.RULEBOOKS)
@submenu_item(MenuItem.Rulebooks.RULEBOOKS)
def rulebook_detail(request, edition_slug, edition_id, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook, id=rulebook_id)
    if (rulebook.slug != rulebook_slug or
                unicode(rulebook.dnd_edition.id) != edition_id or
                rulebook.dnd_edition.slug != edition_slug):
        return permanent_redirect_object(request, rulebook)

    if is_3e_edition(rulebook.dnd_edition):
        request.submenu_item = MenuItem.Rulebooks.BOOKS_3_0
    elif rulebook.dnd_edition.slug == "core-35":
        request.submenu_item = MenuItem.Rulebooks.CORE_3_5
    elif rulebook.dnd_edition.slug == "supplementals-35":
        request.submenu_item = MenuItem.Rulebooks.SUPPLEMENTS_3_5
    elif rulebook.dnd_edition.slug == "dragonlance":
        request.submenu_item = MenuItem.Rulebooks.DRAGONLANCE_3_5
    elif rulebook.dnd_edition.slug == "eberron-35":
        request.submenu_item = MenuItem.Rulebooks.EBERRON_3_5
    elif rulebook.dnd_edition.slug == "forgotten-realms-35":
        request.submenu_item = MenuItem.Rulebooks.FORGOTTEN_REALMS_3_5

    return render_to_response('dnd/rulebooks/rulebook_detail.html',
                              {
                                  'rulebook': rulebook,
                                  'dnd_edition': rulebook.dnd_edition,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )