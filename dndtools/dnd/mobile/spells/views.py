# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from dnd.menu import menu_item, submenu_item
from dnd.mobile.views import permanent_redirect_object_mobile
from dnd.views import is_3e_edition, permanent_redirect_view
from dnd.mobile.dnd_paginator import DndMobilePaginator
from dnd.filters import SpellDomainFilter, SpellDescriptorFilter, SpellFilter
from dnd.models import SpellDescriptor, SpellSchool, SpellSubSchool, Domain, Spell, Rule, Rulebook, DomainVariant


@menu_item("spells")
@submenu_item("spells")
def spell_index_mobile(request):
    f = SpellFilter(request.GET, queryset=Spell.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').distinct())

    paginator = DndMobilePaginator(f.qs, request)

    form_submitted = 1 if '_filter' in request.GET else 0

    return render_to_response('dnd/mobile/spells/spell_index.html',
                              {
                                  'request': request,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item("spells")
@submenu_item("by_rulebooks")
def spell_list_by_rulebook_mobile(request):
    rulebook_list = Rulebook.objects.select_related('dnd_edition').all()

    paginator = DndMobilePaginator(rulebook_list, request)

    return render_to_response('dnd/mobile/spells/spell_list_by_rulebook.html',
                              {
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                              }, context_instance=RequestContext(request), )


@menu_item("spells")
@submenu_item("descriptors")
def spell_descriptor_list_mobile(request):
    f = SpellDescriptorFilter(request.GET,
                              queryset=SpellDescriptor.objects.all())

    paginator = DndMobilePaginator(f.qs, request)

    form_submitted = 1 if '_filter' in request.GET else 0

    return render_to_response('dnd/mobile/spells/spell_descriptor_list.html',
                              {
                                  'request': request,
                                  'spell_descriptor_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item("spells")
@submenu_item("schools")
def spell_school_list_mobile(request):
    spell_school_list = SpellSchool.objects.all()
    spell_sub_school_list = SpellSubSchool.objects.all()
    return render_to_response('dnd/mobile/spells/spell_school_list.html',
                              {
                                  'spell_school_list': spell_school_list,
                                  'spell_sub_school_list': spell_sub_school_list,
                                  'request': request, }, context_instance=RequestContext(request), )


@menu_item("spells")
@submenu_item("by_rulebooks")
def spells_in_rulebook_mobile(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook, pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, spells_in_rulebook_mobile,
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    spell_list = rulebook.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndMobilePaginator(spell_list, request)

    return render_to_response('dnd/mobile/spells/spells_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


@menu_item("spells")
@submenu_item("spells")
def spell_detail_mobile(request, rulebook_slug, rulebook_id, spell_slug, spell_id):
    spell = get_object_or_404(Spell.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school', 'sub_school',
        'class_levels'
    ), pk=spell_id)

    if (spell.slug != spell_slug or
                unicode(spell.rulebook.id) != rulebook_id or
                spell.rulebook.slug != rulebook_slug):
        return permanent_redirect_object_mobile(request, spell)

    spell_class_level_set = spell.spellclasslevel_set.select_related(
        'rulebook', 'character_class',
    ).all()
    spell_domain_level_set = spell.spelldomainlevel_set.select_related(
        'rulebook', 'domain',
    ).all()

    # related spells
    related_spells = Spell.objects.filter(slug=spell.slug).exclude(rulebook__id=spell.rulebook.id).select_related(
        'rulebook').all()

    # corrupt component -- will be linked to corrupt rule
    if spell.corrupt_component:
        corrupt_rule = Rule.objects.filter(slug='corrupt-magic').all()[0]
    else:
        corrupt_rule = None

    return render_to_response('dnd/mobile/spells/spell_detail.html',
                              {
                                  'spell': spell,
                                  'spellclasslevel_set': spell_class_level_set,
                                  'spelldomainlevel_set': spell_domain_level_set,
                                  'corrupt_rule': corrupt_rule,
                                  'rulebook': spell.rulebook,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(spell.rulebook.dnd_edition),
                                  'related_spells': related_spells,
                              },
                              context_instance=RequestContext(request), )


@menu_item("spells")
@submenu_item("descriptors")
def spell_descriptor_detail_mobile(request, spell_descriptor_slug):
    spell_descriptor = get_object_or_404(SpellDescriptor,
                                         slug=spell_descriptor_slug)

    spell_list = spell_descriptor.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndMobilePaginator(spell_list, request)

    return render_to_response('dnd/mobile/spells/spell_descriptor_detail.html',
                              {
                                  'spell_descriptor': spell_descriptor,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


@menu_item("spells")
@submenu_item("schools")
def spell_school_detail_mobile(request, spell_school_slug):
    spell_school = get_object_or_404(SpellSchool, slug=spell_school_slug)

    spell_list = spell_school.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndMobilePaginator(spell_list, request)

    return render_to_response('dnd/mobile/spells/spell_school_detail.html',
                              {
                                  'spell_school': spell_school,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


@menu_item("spells")
@submenu_item("schools")
def spell_sub_school_detail_mobile(request, spell_sub_school_slug):
    spell_sub_school = get_object_or_404(SpellSubSchool,
                                         slug=spell_sub_school_slug)

    spell_list = spell_sub_school.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndMobilePaginator(spell_list, request)

    return render_to_response('dnd/mobile/spells/spell_sub_school_detail.html',
                              {
                                  'spell_sub_school': spell_sub_school,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


@menu_item("spells")
@submenu_item("domains")
def spell_domain_list_mobile(request):
    f = SpellDomainFilter(request.GET, queryset=Domain.objects.all())

    paginator = DndMobilePaginator(f.qs, request)

    form_submitted = 1 if '_filter' in request.GET else 0

    return render_to_response('dnd/mobile/spells/spell_domain_list.html',
                              {
                                  'request': request,
                                  'spell_domain_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item("spells")
@submenu_item("domains")
def spell_domain_detail_mobile(request, spell_domain_slug, rulebook_slug=None, rulebook_id=None):
    # fetch the domain
    spell_domain = get_object_or_404(Domain.objects.select_related(
        'domain_variant', 'domain_variant__rulebook'), slug=spell_domain_slug)

    # fetch primary variant, this is independent of rulebook selected
    try:
        primary_variant = DomainVariant.objects.select_related(
            'rulebook', 'rulebook__dnd_edition',
        ).filter(
            domain=spell_domain,
        ).order_by('-rulebook__dnd_edition__core', '-rulebook__published')[0]
    except Exception:
        primary_variant = None

    # if rulebook is supplied, select find this variant
    if rulebook_slug and rulebook_id:
        # use canonical link in head as this is more or less duplicated content
        selected_variant = get_object_or_404(
            DomainVariant.objects.select_related(
                'domain', 'rulebook', 'rulebook__dnd_edition'),
            domain__slug=spell_domain_slug,
            rulebook__pk=rulebook_id)

        # possible malformed/changed slug
        if rulebook_slug != selected_variant.rulebook.slug:
            return permanent_redirect_object_mobile(request, selected_variant)

        # selected variant is primary! Redirect to canonical url
        if selected_variant == primary_variant:
            return permanent_redirect_view(
                request, spell_domain_detail_mobile, kwargs={
                    'spell_domain_slug': spell_domain_slug}
            )
    else:
        # this is canonical, no need to specify it
        selected_variant = primary_variant

    other_variants = [
        variant
        for variant
        in spell_domain.domainvariant_set.select_related(
            'rulebook', 'rulebook__dnd_edition', 'spell_domain').all()
        if variant != selected_variant
    ]

    if selected_variant:
        display_3e_warning = is_3e_edition(selected_variant.rulebook.dnd_edition)
    else:
        display_3e_warning = False

    spell_list = spell_domain.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndMobilePaginator(spell_list, request)

    return render_to_response('dnd/mobile/spells/spell_domain_detail.html',
                              {
                                  'spell_domain': spell_domain,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'selected_variant': selected_variant,
                                  'other_variants': other_variants,
                                  'display_3e_warning': display_3e_warning,},
                              context_instance=RequestContext(request), )