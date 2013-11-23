# Create your views here.
from datetime import datetime
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from dndtools.dnd.menu import MenuItem
from dndtools.dnd.menu import menu_item, submenu_item
from dndtools.dnd.dnd_paginator import DndPaginator
from dndtools.dnd.filters import SpellFilter, SpellDomainFilter, SpellDescriptorFilter, SpellFilterAdmin
from dndtools.dnd.models import (Rulebook, SpellSchool, SpellDescriptor,
                                 SpellSubSchool, Spell, Domain, Rule, DomainVariant)
from dndtools.dnd.views import is_3e_edition, permanent_redirect_view, permanent_redirect_object, is_admin


@menu_item(MenuItem.MAGIC)
@submenu_item(MenuItem.Magic.SPELLS)
def spell_index(request):
    if is_admin(request):
        f = SpellFilterAdmin(request.GET, queryset=Spell.objects.select_related(
            'rulebook', 'rulebook__dnd_edition', 'school', 'verified_author').distinct())
    else:
        f = SpellFilter(request.GET, queryset=Spell.objects.select_related(
            'rulebook', 'rulebook__dnd_edition', 'school').distinct())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/spells/spell_index.html',
                              {
                                  'request': request,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.MAGIC)
@submenu_item(MenuItem.Magic.DESCRIPTORS)
def spell_descriptor_list(request):
    f = SpellDescriptorFilter(request.GET,
                              queryset=SpellDescriptor.objects.all())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/spells/spell_descriptor_list.html',
                              {
                                  'request': request,
                                  'spell_descriptor_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.MAGIC)
@submenu_item(MenuItem.Magic.SCHOOLS)
def spell_school_list(request):
    spell_school_list = SpellSchool.objects.all()
    spell_sub_school_list = SpellSubSchool.objects.all()
    return render_to_response('dnd/spells/spell_school_list.html',
                              {
                                  'spell_school_list': spell_school_list,
                                  'spell_sub_school_list': spell_sub_school_list,
                                  'request': request, }, context_instance=RequestContext(request), )


@menu_item(MenuItem.MAGIC)
@submenu_item(MenuItem.Magic.SPELLS)
def spells_in_rulebook(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook, pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, 'spells_in_rulebook',
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    spell_list = rulebook.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndPaginator(spell_list, request)

    return render_to_response('dnd/spells/spells_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.MAGIC)
@submenu_item(MenuItem.Magic.SPELLS)
def spell_detail(request, rulebook_slug, rulebook_id, spell_slug, spell_id):
    spell = get_object_or_404(Spell.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school', 'sub_school',
        'class_levels'
    ), pk=spell_id)

    if (spell.slug != spell_slug or
                unicode(spell.rulebook.id) != rulebook_id or
                spell.rulebook.slug != rulebook_slug):
        return permanent_redirect_object(request, spell)

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

    return render_to_response('dnd/spells/spell_detail.html',
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


def spell_verify(request, spell_id):
    if not is_admin(request):
        return HttpResponseForbidden("Forbidden.")

    spell = get_object_or_404(Spell, id=spell_id)

    spell.verified = True
    spell.verified_time = datetime.now()
    spell.verified_author = request.user
    spell.save()

    return permanent_redirect_object(request, spell)


@menu_item(MenuItem.MAGIC)
@submenu_item(MenuItem.Magic.DESCRIPTORS)
def spell_descriptor_detail(request, spell_descriptor_slug):
    spell_descriptor = get_object_or_404(SpellDescriptor,
                                         slug=spell_descriptor_slug)

    spell_list = spell_descriptor.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndPaginator(spell_list, request)

    return render_to_response('dnd/spells/spell_descriptor_detail.html',
                              {
                                  'spell_descriptor': spell_descriptor,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


@menu_item(MenuItem.MAGIC)
@submenu_item(MenuItem.Magic.SCHOOLS)
def spell_school_detail(request, spell_school_slug):
    spell_school = get_object_or_404(SpellSchool, slug=spell_school_slug)

    spell_list = spell_school.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndPaginator(spell_list, request)

    return render_to_response('dnd/spells/spell_school_detail.html',
                              {
                                  'spell_school': spell_school,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


@menu_item(MenuItem.MAGIC)
@submenu_item(MenuItem.Magic.SCHOOLS)
def spell_sub_school_detail(request, spell_sub_school_slug):
    spell_sub_school = get_object_or_404(SpellSubSchool,
                                         slug=spell_sub_school_slug)

    spell_list = spell_sub_school.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndPaginator(spell_list, request)

    return render_to_response('dnd/spells/spell_sub_school_detail.html',
                              {
                                  'spell_sub_school': spell_sub_school,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


@menu_item(MenuItem.MAGIC)
@submenu_item(MenuItem.Magic.DOMAINS)
def spell_domain_list(request):
    f = SpellDomainFilter(request.GET, queryset=Domain.objects.all())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/spells/spell_domain_list.html',
                              {
                                  'request': request,
                                  'spell_domain_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.MAGIC)
@submenu_item(MenuItem.Magic.DOMAINS)
def spell_domain_detail(request, spell_domain_slug, rulebook_slug=None, rulebook_id=None):
    # fetch the class
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
        use_canonical_link = True
        selected_variant = get_object_or_404(
            DomainVariant.objects.select_related(
                'domain', 'rulebook', 'rulebook__dnd_edition'),
            domain__slug=spell_domain_slug,
            rulebook__pk=rulebook_id)

        # possible malformed/changed slug
        if rulebook_slug != selected_variant.rulebook.slug:
            return permanent_redirect_object(request, selected_variant)

        # selected variant is primary! Redirect to canonical url
        if selected_variant == primary_variant:
            return permanent_redirect_view(
                request, spell_domain_detail, kwargs={
                    'spell_domain_slug': spell_domain_slug}
            )
    else:
        # this is canonical, no need to specify it
        use_canonical_link = False
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

    paginator = DndPaginator(spell_list, request)

    return render_to_response('dnd/spells/spell_domain_detail.html',
                              {
                                  'spell_domain': spell_domain,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'selected_variant': selected_variant,
                                  'other_variants': other_variants,
                                  'use_canonical_link': use_canonical_link,
                                  'display_3e_warning': display_3e_warning, },
                              context_instance=RequestContext(request), )
