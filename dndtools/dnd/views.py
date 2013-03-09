# Create your views here.
from math import ceil
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from reversion.revisions import revision
from dndtools.dnd.dnd_paginator import DndPaginator
from dndtools.dnd.filters import (SpellFilter, CharacterClassFilter, RulebookFilter, FeatFilter, SpellDomainFilter,
                                  SpellDescriptorFilter, SkillFilter, RaceFilter, MonsterFilter, ItemFilter, LanguageFilter)
from dndtools.dnd.forms import ContactForm, InaccurateContentForm

from dndtools.dnd.models import (Rulebook, DndEdition, FeatCategory, Feat,
                                 SpellSchool, SpellDescriptor, SpellSubSchool,
                                 Spell, CharacterClass, Domain, CharacterClassVariant, Skill, Race, SkillVariant,
                                 NewsEntry, StaticPage, Monster, Rule, Item, Language)
from dndtools.dnd.utilities import int_with_commas


def permanent_redirect_view(request, view_name, args=None, kwargs=None):
    url = reverse(view_name, args=args, kwargs=kwargs)
    # get parameters
    if len(request.GET) > 0:
        #noinspection PyUnresolvedReferences
        url += "?" + request.GET.urlencode()

    return HttpResponsePermanentRedirect(url)


# noinspection PyShadowingBuiltins
def permanent_redirect_object(request, object):
    url = object.get_absolute_url()
    # get parameters
    if len(request.GET) > 0:
        #noinspection PyUnresolvedReferences
        url += "?" + request.GET.urlencode()

    return HttpResponsePermanentRedirect(url)


def is_3e_edition(edition):
    return edition.system == 'DnD 3.0'


def index(request):
    newsEntries = NewsEntry.objects.filter(enabled=True).order_by('-published')[:15]

    response = render_to_response('dnd/index.html',
                                  {
                                      'request': request, 'newsEntries': newsEntries,
                                  },
                                  context_instance=RequestContext(request), )

    if len(newsEntries):
        response.set_cookie('top_news', newsEntries[0].pk, 10 * 365 * 24 * 60 * 60)

    return response


def rulebook_list(request):
    f = RulebookFilter(request.GET, queryset=Rulebook.objects.select_related(
        'dnd_edition'))

    form_submitted = 1 if 'name' in request.GET else 0

    paginator = DndPaginator(f.qs, request)

    return render_to_response('dnd/rulebook_list.html',
                              {
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


def edition_list(request):
    edition_list = DndEdition.objects.all()

    paginator = DndPaginator(edition_list, request)

    return render_to_response('dnd/edition_list.html',
                              {
                                  'edition_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                              }, context_instance=RequestContext(request), )


def edition_detail(request, edition_slug, edition_id):
    dnd_edition = get_object_or_404(DndEdition, id=edition_id)
    if dnd_edition.slug != edition_slug:
        return permanent_redirect_view(request, 'edition_detail',
                                       kwargs={
                                           'edition_slug': dnd_edition.slug,
                                           'edition_id': dnd_edition.id, })

    rulebook_list = dnd_edition.rulebook_set.select_related('dnd_edition').all()

    paginator = DndPaginator(rulebook_list, request)

    return render_to_response('dnd/edition_detail.html',
                              {
                                  'dnd_edition': dnd_edition,
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(dnd_edition),
                              }, context_instance=RequestContext(request), )


def rulebook_detail(request, edition_slug, edition_id, rulebook_slug,
                    rulebook_id):
    rulebook = get_object_or_404(Rulebook, id=rulebook_id)
    if (rulebook.slug != rulebook_slug or
                unicode(rulebook.dnd_edition.id) != edition_id or
                rulebook.dnd_edition.slug != edition_slug):
        return permanent_redirect_view(
            request, 'rulebook_detail',
            kwargs={
                'edition_slug': rulebook.dnd_edition.slug,
                'edition_id': rulebook.dnd_edition.id,
                'rulebook_slug': rulebook.slug,
                'rulebook_id': rulebook.id, })

    return render_to_response('dnd/rulebook_detail.html',
                              {
                                  'rulebook': rulebook,
                                  'dnd_edition': rulebook.dnd_edition,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


def feat_index(request):
    f = FeatFilter(request.GET, queryset=Feat.objects.select_related(
        'rulebook', 'rulebook__dnd_edition').distinct())

    form_submitted = 1 if 'name' in request.GET else 0

    paginator = DndPaginator(f.qs, request)

    return render_to_response('dnd/feat_index.html',
                              {
                                  'request': request,
                                  'feat_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


def feat_list_by_rulebook(request):
    rulebook_list = Rulebook.objects.select_related('rulebook',
                                                    'dnd_edition').all()

    paginator = DndPaginator(rulebook_list, request)

    return render_to_response('dnd/feat_list_by_rulebook.html',
                              {
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request, }, context_instance=RequestContext(request), )


def feat_category_list(request):
    feat_category_list = FeatCategory.objects.all()

    paginator = DndPaginator(feat_category_list, request)

    return render_to_response('dnd/feat_category_list.html',
                              {
                                  'feat_category_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request, }, context_instance=RequestContext(request), )


def feat_category_detail(request, category_slug):
    feat_category = get_object_or_404(FeatCategory, slug=category_slug)
    feat_list = feat_category.feat_set.select_related('rulebook',
                                                      'rulebook__dnd_edition').all()

    paginator = DndPaginator(feat_list, request)

    return render_to_response('dnd/feat_category_detail.html',
                              {
                                  'feat_category': feat_category,
                                  'feat_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


def feats_in_rulebook(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook.objects.select_related('dnd_edition'),
                                 pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, 'feats_in_rulebook',
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    feat_list = rulebook.feat_set.select_related('rulebook',
                                                 'rulebook__dnd_edition').all()

    paginator = DndPaginator(feat_list, request)

    return render_to_response('dnd/feats_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'feat_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


def feat_detail(request, rulebook_slug, rulebook_id, feat_slug, feat_id):
    feat = get_object_or_404(
        Feat.objects.select_related('rulebook', 'rulebook__dnd_edition'),
        pk=feat_id)
    if (feat.slug != feat_slug or
                unicode(feat.rulebook.id) != rulebook_id or
                feat.rulebook.slug != rulebook_slug):
        return permanent_redirect_view(request, 'feat_detail',
                                       kwargs={
                                           'rulebook_slug': feat.rulebook.slug,
                                           'rulebook_id': feat.rulebook.id,
                                           'feat_slug': feat.slug,
                                           'feat_id': feat.id, })

    feat_category_list = feat.feat_categories.select_related().all()
    required_feats = feat.required_feats.select_related('required_feat',
                                                        'required_feat__rulebook').all()
    required_by_feats = feat.required_by_feats.select_related('source_feat',
                                                              'source_feat__rulebook').all()
    required_skills = feat.required_skills.select_related('skill').all()
    special_prerequisities = feat.featspecialfeatprerequisite_set.select_related(
        'special_feat_prerequisite').all()
    # related feats
    related_feats = Feat.objects.filter(slug=feat.slug).exclude(rulebook__id=feat.rulebook.id).select_related(
        'rulebook', 'rulebook__dnd_edition').all()

    return render_to_response('dnd/feat_detail.html',
                              {
                                  'feat': feat,
                                  'rulebook': feat.rulebook,
                                  'feat_category_list': feat_category_list,
                                  'required_feats': required_feats,
                                  'required_by_feats': required_by_feats,
                                  'required_skills': required_skills,
                                  'special_prerequisities': special_prerequisities,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(feat.rulebook.dnd_edition),
                                  'related_feats': related_feats,
                              }, context_instance=RequestContext(request), )


def spell_index(request):
    f = SpellFilter(request.GET, queryset=Spell.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').distinct())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/spell_index.html',
                              {
                                  'request': request,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


def spell_list_by_rulebook(request):
    rulebook_list = Rulebook.objects.select_related('dnd_edition').all()

    paginator = DndPaginator(rulebook_list, request)

    return render_to_response('dnd/spell_list_by_rulebook.html',
                              {
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                              }, context_instance=RequestContext(request), )


def spell_descriptor_list(request):
    f = SpellDescriptorFilter(request.GET,
                              queryset=SpellDescriptor.objects.all())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/spell_descriptor_list.html',
                              {
                                  'request': request,
                                  'spell_descriptor_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


def spell_school_list(request):
    spell_school_list = SpellSchool.objects.all()
    spell_sub_school_list = SpellSubSchool.objects.all()
    return render_to_response('dnd/spell_school_list.html',
                              {
                                  'spell_school_list': spell_school_list,
                                  'spell_sub_school_list': spell_sub_school_list,
                                  'request': request, }, context_instance=RequestContext(request), )


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

    return render_to_response('dnd/spells_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


def spell_detail(request, rulebook_slug, rulebook_id, spell_slug, spell_id):
    spell = get_object_or_404(Spell.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school', 'sub_school',
        'class_levels'
    ), pk=spell_id)

    if (spell.slug != spell_slug or
                unicode(spell.rulebook.id) != rulebook_id or
                spell.rulebook.slug != rulebook_slug):
        return permanent_redirect_view(
            request, 'spell_detail', kwargs={
                'rulebook_slug': spell.rulebook.slug,
                'rulebook_id': spell.rulebook.id,
                'spell_slug': spell.slug,
                'spell_id': spell_id,
            }
        )

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

    return render_to_response('dnd/spell_detail.html',
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


def spell_descriptor_detail(request, spell_descriptor_slug):
    spell_descriptor = get_object_or_404(SpellDescriptor,
                                         slug=spell_descriptor_slug)

    spell_list = spell_descriptor.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndPaginator(spell_list, request)

    return render_to_response('dnd/spell_descriptor_detail.html',
                              {
                                  'spell_descriptor': spell_descriptor,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


def spell_school_detail(request, spell_school_slug):
    spell_school = get_object_or_404(SpellSchool, slug=spell_school_slug)

    spell_list = spell_school.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndPaginator(spell_list, request)

    return render_to_response('dnd/spell_school_detail.html',
                              {
                                  'spell_school': spell_school,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


def spell_sub_school_detail(request, spell_sub_school_slug):
    spell_sub_school = get_object_or_404(SpellSubSchool,
                                         slug=spell_sub_school_slug)

    spell_list = spell_sub_school.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndPaginator(spell_list, request)

    return render_to_response('dnd/spell_sub_school_detail.html',
                              {
                                  'spell_sub_school': spell_sub_school,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


def spell_domain_list(request):
    f = SpellDomainFilter(request.GET, queryset=Domain.objects.all())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/spell_domain_list.html',
                              {
                                  'request': request,
                                  'spell_domain_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


def spell_domain_detail(request, spell_domain_slug):
    spell_domain = get_object_or_404(Domain,
                                     slug=spell_domain_slug)

    spell_list = spell_domain.spell_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndPaginator(spell_list, request)

    return render_to_response('dnd/spell_domain_detail.html',
                              {
                                  'spell_domain': spell_domain,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


def character_class_list(request):
    f = CharacterClassFilter(
        request.GET,
        queryset=CharacterClass.objects.select_related(
            'rulebook', 'rulebook__dnd_edition')
    )

    form_submitted = 1 if 'name' in request.GET else 0

    paginator = DndPaginator(f.qs, request)

    return render_to_response('dnd/character_class_list.html',
                              {
                                  'character_class_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


def character_class_detail(request, character_class_slug, rulebook_slug=None,
                           rulebook_id=None):
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
            return permanent_redirect_object(request, selected_variant)

        # selected variant is primary! Redirect to canonical url
        if selected_variant == primary_variant:
            return permanent_redirect_view(
                request, character_class_detail, kwargs={
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

    return render_to_response('dnd/character_class_detail.html',
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


def character_class_spells(request, character_class_slug, level):
    character_class = get_object_or_404(CharacterClass,
                                        slug=character_class_slug)

    spell_list = Spell.objects.filter(
        spellclasslevel__character_class=character_class.id,
        spellclasslevel__level=level).select_related(
        'rulebook',
        'rulebook__dnd_edition',
        'school')

    paginator = DndPaginator(spell_list, request)

    return render_to_response('dnd/character_class_spells.html',
                              {
                                  'character_class': character_class,
                                  'spell_list': paginator.items(),
                                  'paginator': paginator,
                                  'level': level,
                                  'request': request, }, context_instance=RequestContext(request),
    )


def character_classes_in_rulebook(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook, pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, 'character_classes_in_rulebook',
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    class_list = [
        character_class_variant.character_class
        for character_class_variant
        in rulebook.characterclassvariant_set.select_related('character_class').all()
    ]

    return render_to_response('dnd/character_classes_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'class_list': class_list,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


def skill_list(request):
    f = SkillFilter(request.GET, queryset=Skill.objects.all())

    form_submitted = 1 if 'name' in request.GET else 0

    paginator = DndPaginator(f.qs, request)

    return render_to_response('dnd/skill_list.html',
                              {
                                  'request': request,
                                  'skill_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


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

    return render_to_response('dnd/skill_detail.html',
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

    return render_to_response('dnd/skill_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'skill_list': skill_list,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


def monster_index(request):
    f = MonsterFilter(request.GET, queryset=Monster.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').distinct())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/monster_index.html',
                              {
                                  'request': request,
                                  'monster_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


def monster_list_by_rulebook(request):
    rulebook_list = Rulebook.objects.select_related('dnd_edition').all()

    paginator = DndPaginator(rulebook_list, request)

    return render_to_response('dnd/monster_list_by_rulebook.html',
                              {
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                              }, context_instance=RequestContext(request), )


def monsters_in_rulebook(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook, pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, 'monsters_in_rulebook',
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    monster_list = rulebook.monster_set.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').all()

    paginator = DndPaginator(monster_list, request)

    return render_to_response('dnd/monsters_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'monster_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


def monster_detail(request, rulebook_slug, rulebook_id, monster_slug, monster_id):
    monster = get_object_or_404(
        Monster.objects.select_related('rulebook', 'rulebook__dnd_edition', 'size',
                                       'type', ),
        pk=monster_id)
    if (monster.slug != monster_slug or
                unicode(monster.rulebook.id) != rulebook_id or
                monster.rulebook.slug != rulebook_slug):
        return permanent_redirect_view(request, 'monster_detail',
                                       kwargs={
                                           'rulebook_slug': monster.rulebook.slug,
                                           'rulebook_id': monster.rulebook.id,
                                           'monster_slug': monster.slug,
                                           'monster_id': monster.id, })

    if False:
        monster = Monster()

    monster_speeds = monster.monsterspeed_set.select_related('type', ).all()
    monster_subtypes = monster.subtypes.all()
    monster_skills = monster.skills.select_related('skill').all()
    monster_feats = monster.feats.select_related('feat', 'feat__rulebook').all()

    return render_to_response('dnd/monster_detail.html',
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


def race_index(request):
    f = RaceFilter(request.GET, queryset=Race.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'school').distinct())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/race_index.html',
                              {
                                  'request': request,
                                  'race_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


def race_list_by_rulebook(request):
    rulebook_list = Rulebook.objects.select_related('dnd_edition').all()

    paginator = DndPaginator(rulebook_list, request)

    return render_to_response('dnd/race_list_by_rulebook.html',
                              {
                                  'request': request,
                                  'rulebook_list': paginator.items(),
                                  'paginator': paginator,
                              }, context_instance=RequestContext(request), )


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

    return render_to_response('dnd/races_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'race_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


def race_detail(request, rulebook_slug, rulebook_id, race_slug, race_id):
    race = get_object_or_404(
        Race.objects.select_related('rulebook', 'rulebook__dnd_edition', 'size', 'automatic_languages',
                                    'bonus_languages'),
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

    return render_to_response('dnd/race_detail.html',
                              {
                                  'race': race,
                                  'rulebook': race.rulebook,
                                  'request': request,
                                  'race_speeds': race_speeds,
                                  'favored_classes': favored_classes,
                                  'automatic_languages': race.automatic_languages.all(),
                                  'bonus_languages': race.bonus_languages.all(),
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(race.rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


def item_index(request):
    f = ItemFilter(request.GET, queryset=Item.objects.select_related(
        'rulebook', 'rulebook__dnd_edition').distinct())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/item_index.html',
                              {
                                  'request': request,
                                  'item_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


def item_detail(request, rulebook_slug, rulebook_id, item_slug, item_id):
    item = get_object_or_404(Item.objects.select_related(
        'rulebook', 'rulebook__dnd_edition', 'body_slot', 'aura', 'spellschool_set',
        'activation', 'required_feats', 'required_spells', 'property', 'synergy_prerequisite',
    ), pk=item_id)
    assert isinstance(item, Item)

    if (item.slug != item_slug or
                unicode(item.rulebook.id) != rulebook_id or
                item.rulebook.slug != rulebook_slug):
        return permanent_redirect_view(
            request, 'item_detail', kwargs={
                'rulebook_slug': item.rulebook.slug,
                'rulebook_id': item.rulebook.id,
                'item_slug': item.slug,
                'item_id': item_id,
            }
        )

    required_feats = item.required_feats.select_related('rulebook').all()
    required_spells = item.required_spells.select_related('rulebook').all()

    cost_to_create = item.cost_to_create
    # calculate CTC
    if not cost_to_create:
        if item.price_gp and not item.price_bonus:
            cost_to_create = "%s gp, %s XP, %d day(s)" % (
                int_with_commas(ceil(item.price_gp / 2.0)), int_with_commas(ceil(item.price_gp / 25.0)),
                ceil(item.price_gp / 1000.0))
        elif not item.price_gp and item.price_bonus:
            cost_to_create = "Varies"

    return render_to_response('dnd/item_detail.html',
                              {
                                  'item': item,
                                  'aura_schools': item.aura_schools.all(),
                                  'required_feats': required_feats,
                                  'required_spells': required_spells,
                                  'cost_to_create': cost_to_create,
                                  'rulebook': item.rulebook,
                                  'request': request,
                                  # enum
                                  'ItemType': Item.ItemType,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(item.rulebook.dnd_edition),
                              },
                              context_instance=RequestContext(request), )


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST,
                           initial={
                               'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            if form.cleaned_data['sender']:
                headers = {
                    'Reply-To': form.cleaned_data['sender']}
            else:
                headers = {}

            email = EmailMessage(
                subject=form.cleaned_data['subject'],
                body="%s\n\nfrom: %s" % (form.cleaned_data['message'],
                                         form.cleaned_data['sender']),
                from_email='mailer@dndtools.eu',
                to=('dndtoolseu@googlegroups.com', 'dndtools.eu@gmail.com'),
                headers=headers,
            )

            email.send()

            # Redirect after POST
            return HttpResponseRedirect(reverse('contact_sent'))

    else:
        form = ContactForm()  # An unbound form

    # request context required for CSRF
    return render_to_response('dnd/contact.html',
                              {
                                  'request': request,
                                  'form': form, }, context_instance=RequestContext(request), )


def contact_sent(request):
    return render_to_response('dnd/contact_sent.html',
                              {
                                  'request': request,
                              }, context_instance=RequestContext(request), )


def inaccurate_content(request):
    if request.method == 'POST':
        form = InaccurateContentForm(request.POST, initial={
            'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            if form.cleaned_data['sender']:
                headers = {
                    'Reply-To': form.cleaned_data['sender']}
            else:
                headers = {}

            email = EmailMessage(
                subject='Problem in url %s' % form.cleaned_data['url'],
                body="Message: %s\n\nUrl: %s\n\nBetter desc:%s\nFrom: %s" % (
                    form.cleaned_data['message'], form.cleaned_data['url'],
                    form.cleaned_data['better_description'],
                    form.cleaned_data['sender']),
                from_email='mailer@dndtools.eu',
                to=('dndtoolseu@googlegroups.com', 'dndtools.eu@gmail.com'),
                headers=headers,
            )

            email.send()

            # Redirect after POST
            return HttpResponseRedirect(reverse('inaccurate_content_sent'))

    else:
        form = InaccurateContentForm(
            initial={
                'url': request.GET.get('url', ''),
            })

    return render_to_response('dnd/inaccurate_content.html',
                              {
                                  'request': request,
                                  'form': form, }, context_instance=RequestContext(request), )


def inaccurate_content_sent(request):
    return render_to_response('dnd/inaccurate_content_sent.html',
                              {
                                  'request': request,
                              }, context_instance=RequestContext(request), )


def staff(request):
    page_body = StaticPage.objects.filter(name='staff')[0]

    return render_to_response('dnd/staff.html',
                              {
                                  'request': request,
                                  'page_body': page_body,
                              }, context_instance=RequestContext(request), )


@revision.create_on_success
def very_secret_url(request):
    log = ''

    #noinspection PyUnresolvedReferences
    revision.comment = "Automatic (updating PHB spell pages)"
    #noinspection PyUnresolvedReferences
    revision.user = User.objects.get(username='dndtools')

    #    counter = 1
    #
    #    phb = Rulebook.objects.get(abbr='PH')
    #
    #    for line in data.split('\n'):
    #        line = line.strip()
    #        m = re.match('([^\t]+)\tPH \t(\d+)', line)
    #        if m:
    #            spells = Spell.objects.filter(rulebook=phb, slug=slugify(m.group(1).strip()))
    #            spell = spells[0] if spells else None
    #
    #            if spell and spell.page is None:
    #                spell.page = m.group(2).strip()
    #                spell.save()
    #
    #                message = '%05d %s saved\n' % (counter, spell)
    #                log += message
    #                print message,
    #                counter += 1
    #            else:
    #                message = '%05d %s IGNORED\n' % (counter, spell)
    #                log += message
    #                print message,
    #                counter += 1

    return render_to_response('dnd/very_secret_url.html',
                              {
                                  'request': request,
                                  'log': log,
                              }, context_instance=RequestContext(request), )


def rule_detail(request, rulebook_slug, rulebook_id, rule_slug, rule_id):
    rule = get_object_or_404(
        Rule.objects.select_related('rulebook', 'rulebook__dnd_edition'),
        pk=rule_id)
    if (rule.slug != rule_slug or
                unicode(rule.rulebook.id) != rulebook_id or
                rule.rulebook.slug != rulebook_slug):
        return permanent_redirect_view(request, 'rule_detail',
                                       kwargs={
                                           'rulebook_slug': rule.rulebook.slug,
                                           'rulebook_id': rule.rulebook.id,
                                           'rule_slug': rule.slug,
                                           'rule_id': rule.id, })

    return render_to_response('dnd/rule_detail.html',
                              {
                                  'rule': rule,
                                  'rulebook': rule.rulebook,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(rule.rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


def language_index(request):
    f = LanguageFilter(request.GET, queryset=Language.objects.distinct())

    paginator = DndPaginator(f.qs, request)

    form_submitted = 1 if 'name' in request.GET else 0

    return render_to_response('dnd/language_index.html',
                              {
                                  'request': request,
                                  'language_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


def language_detail(request, language_slug):
    language = get_object_or_404(
        Language.objects, slug=language_slug,
    )
    assert isinstance(language, Language)

    race_list = Race.objects.filter(Q(automatic_languages=language) | Q(bonus_languages=language)).select_related(
        'rulebook').distinct().all()

    paginator = DndPaginator(race_list, request)

    return render_to_response('dnd/language_detail.html',
                              {
                                  'language': language,
                                  'paginator': paginator,
                                  'race_list': race_list,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                              }, context_instance=RequestContext(request), )