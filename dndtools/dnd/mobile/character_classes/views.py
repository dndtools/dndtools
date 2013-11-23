# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from dndtools.dnd.menu import menu_item
from dndtools.dnd.filters import CharacterClassFilter
from dndtools.dnd.mobile.dnd_paginator import DndMobilePaginator
from dndtools.dnd.mobile.views import permanent_redirect_object_mobile
from dndtools.dnd.models import Rulebook, Spell, CharacterClass, CharacterClassVariant
from dndtools.dnd.views import permanent_redirect_view, is_3e_edition


@menu_item("classes")
def character_class_list_mobile(request):
    f = CharacterClassFilter(
        request.GET,
        queryset=CharacterClassVariant.objects.select_related(
            'rulebook', 'rulebook__dnd_edition', 'character_class')
    )

    form_submitted = 1 if 'name' in request.GET else 0

    paginator = DndMobilePaginator(f.qs, request)

    return render_to_response('dnd/mobile/character_classes/character_class_list.html',
                              {
                                  'character_class_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item("classes")
def character_class_detail_mobile(request, character_class_slug, rulebook_slug=None, rulebook_id=None):
    # fetch the class
    character_class = get_object_or_404(
        CharacterClass.objects.select_related('character_class_variant', 'character_class_variant__rulebook'),
        slug=character_class_slug)

    assert isinstance(character_class, CharacterClass)

    # fetch primary variant, this is independent of rulebook selected
    try:
        primary_variant = CharacterClassVariant.objects.select_related(
            'rulebook', 'rulebook__dnd_edition',
        ).filter(
            character_class=character_class,
        ).order_by('-rulebook__dnd_edition__core', '-rulebook__published')[0]
    except Exception:
        primary_variant = None

    # if rulebook is supplied, select find this variant
    if rulebook_slug and rulebook_id:
        # use canonical link in head as this is more or less duplicated content
        use_canonical_link = True
        selected_variant = get_object_or_404(
            CharacterClassVariant.objects.select_related(
                'rulebook', 'character_class', 'rulebook__dnd_edition'),
            character_class__slug=character_class_slug,
            rulebook__pk=rulebook_id)

        # possible malformed/changed slug
        if rulebook_slug != selected_variant.rulebook.slug:
            return permanent_redirect_object_mobile(request, selected_variant)

        # selected variant is primary! Redirect to canonical url
        if selected_variant == primary_variant:
            return permanent_redirect_view(
                request, character_class_detail_mobile, kwargs={
                    'character_class_slug': character_class_slug}
            )
    else:
        # this is canonical, no need to specify it
        use_canonical_link = False
        selected_variant = primary_variant

    other_variants = [
        variant
        for variant
        in character_class.characterclassvariant_set.select_related(
            'rulebook', 'rulebook__dnd_edition', 'character_class').all()
        if variant != selected_variant
    ]

    if selected_variant:
        required_races = selected_variant.required_races.select_related('race', 'race__rulebook').all()
        required_skills = selected_variant.required_skills.select_related('skill').all()
        required_feats = selected_variant.required_feats.select_related('feat', 'feat__rulebook').all()
        display_3e_warning = is_3e_edition(selected_variant.rulebook.dnd_edition)
    else:
        required_races = ()
        required_skills = ()
        required_feats = ()
        display_3e_warning = False

    return render_to_response('dnd/mobile/character_classes/character_class_detail.html',
                              {
                                  'character_class': character_class,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'selected_variant': selected_variant,
                                  'required_races': required_races,
                                  'required_skills': required_skills,
                                  'required_feats': required_feats,
                                  'other_variants': other_variants,
                                  'use_canonical_link': use_canonical_link,
                                  'display_3e_warning': display_3e_warning,
                              }, context_instance=RequestContext(request), )


@menu_item("classes")
def character_class_spells_mobile(request, character_class_slug, level):
    character_class = get_object_or_404(CharacterClass,
                                        slug=character_class_slug)

    spell_list = Spell.objects.filter(
        spellclasslevel__character_class=character_class.id,
        spellclasslevel__level=level).select_related(
        'rulebook',
        'rulebook__dnd_edition',
        'school')

    paginator = DndMobilePaginator(spell_list, request)

    return render_to_response('dnd/mobile/character_classes/character_class_spells.html',
                              {
                                  'character_class': character_class,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'level': level,
                                  'request': request, }, context_instance=RequestContext(request),
    )


@menu_item("classes")
def character_classes_in_rulebook_mobile(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook, pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, character_classes_in_rulebook_mobile,
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    class_list = [
        character_class_variant.character_class
        for character_class_variant
        in rulebook.characterclassvariant_set.select_related('character_class').all()
    ]

    return render_to_response('dnd/mobile/character_classes/character_classes_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'class_list': class_list,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )