# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from dnd.menu import MenuItem, menu_item, submenu_item
from dnd.views import permanent_redirect_object, permanent_redirect_view, is_3e_edition
from dnd.dnd_paginator import DndPaginator
from dnd.filters import SkillFilter

from dnd.models import Rulebook, Skill, SkillVariant

@menu_item(MenuItem.CHARACTER_OPTIONS)
@submenu_item(MenuItem.CharacterOptions.SKILLS)
def skill_list(request):
    f = SkillFilter(request.GET, queryset=Skill.objects.all())

    form_submitted = 1 if '_filter' in request.GET else 0

    paginator = DndPaginator(f.qs, request)

    return render_to_response('dnd/skills/skill_list.html',
                              {
                                  'request': request,
                                  'skill_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.CHARACTER_OPTIONS)
@submenu_item(MenuItem.CharacterOptions.SKILLS)
def skill_detail(request, skill_slug, rulebook_slug=None,
                 rulebook_id=None):
    # fetch the class
    skill = get_object_or_404(Skill.objects.select_related(
        'skill_variant', 'skill_variant__rulebook'), slug=skill_slug)

    # fetch primary variant, this is independent of rulebook selected
    try:
        primary_variant = SkillVariant.objects.select_related(
            'rulebook', 'rulebook__dnd_edition',
        ).filter(
            skill=skill,
        ).order_by('-rulebook__dnd_edition__core', '-rulebook__published')[0]
    except Exception:
        primary_variant = None

    # if rulebook is supplied, select find this variant
    if rulebook_slug and rulebook_id:
        # use canonical link in head as this is more or less duplicated content
        use_canonical_link = True
        selected_variant = get_object_or_404(
            SkillVariant.objects.select_related(
                'rulebook', 'skill', 'rulebook__dnd_edition'),
            skill__slug=skill_slug,
            rulebook__pk=rulebook_id)

        # possible malformed/changed slug
        if rulebook_slug != selected_variant.rulebook.slug:
            return permanent_redirect_object(request, selected_variant)

        # selected variant is primary! Redirect to canonical url
        if selected_variant == primary_variant:
            return permanent_redirect_view(
                request, skill_detail, kwargs={
                    'skill_slug': skill_slug}
            )
    else:
        # this is canonical, no need to specify it
        use_canonical_link = False
        selected_variant = primary_variant

    other_variants = [
        variant
        for variant
        in skill.skillvariant_set.select_related(
            'rulebook', 'rulebook__dnd_edition', 'skill').all()
        if variant != selected_variant
    ]

    if selected_variant:
        display_3e_warning = is_3e_edition(selected_variant.rulebook.dnd_edition)
    else:
        display_3e_warning = False

    feat_list = skill.required_by_feats.select_related('rulebook').all()
    feat_paginator = DndPaginator(feat_list, request)

    return render_to_response('dnd/skills/skill_detail.html',
                              {
                                  'skill': skill,
                                  'feat_list': feat_paginator.items(),
                                  'feat_paginator': feat_paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'selected_variant': selected_variant,
                                  'other_variants': other_variants,
                                  'use_canonical_link': use_canonical_link,
                                  'display_3e_warning': display_3e_warning,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.CHARACTER_OPTIONS)
@submenu_item(MenuItem.CharacterOptions.SKILLS)
def skills_in_rulebook(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook, pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, 'skills_in_rulebook',
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    skill_list = [
        skill_variant.skill
        for skill_variant
        in rulebook.skillvariant_set.all()
    ]

    return render_to_response('dnd/skills/skill_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'skill_list': skill_list,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )