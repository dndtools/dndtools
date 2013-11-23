# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from dndtools.dnd.menu import menu_item, submenu_item
from dndtools.dnd.mobile.views import permanent_redirect_object_mobile
from dndtools.dnd.mobile.dnd_paginator import DndMobilePaginator
from dndtools.dnd.filters import FeatFilter
from dndtools.dnd.models import Feat, Rulebook, FeatCategory
from dndtools.dnd.views import is_3e_edition, permanent_redirect_view


@menu_item("feats")
@submenu_item("feats")
def feat_index_mobile(request):
    f = FeatFilter(request.GET, queryset=Feat.objects.select_related(
        'rulebook', 'rulebook__dnd_edition').distinct())

    form_submitted = 1 if 'name' in request.GET else 0

    paginator = DndMobilePaginator(f.qs, request)

    return render_to_response('dnd/mobile/feats/feat_index.html',
                              {
                                  'request': request,
                                  'feat_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item("feats")
@submenu_item("categories")
def feat_category_list_mobile(request):
    feat_category_list = FeatCategory.objects.all()

    paginator = DndMobilePaginator(feat_category_list, request)

    return render_to_response('dnd/mobile/feats/feat_category_list.html',
                              {
                                  'feat_category_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request, }, context_instance=RequestContext(request), )


@menu_item("feats")
@submenu_item("categories")
def feat_category_detail_mobile(request, category_slug):
    feat_category = get_object_or_404(FeatCategory, slug=category_slug)
    feat_list = feat_category.feat_set.select_related('rulebook',
                                                      'rulebook__dnd_edition').all()

    paginator = DndMobilePaginator(feat_list, request)

    return render_to_response('dnd/mobile/feats/feat_category_detail.html',
                              {
                                  'feat_category': feat_category,
                                  'feat_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(), },
                              context_instance=RequestContext(request), )


@menu_item("feats")
@submenu_item("by_rulebooks")
def feats_in_rulebook_mobile(request, rulebook_slug, rulebook_id):
    rulebook = get_object_or_404(Rulebook.objects.select_related('dnd_edition'),
                                 pk=rulebook_id)
    if not rulebook.slug == rulebook_slug:
        return permanent_redirect_view(request, feats_in_rulebook_mobile,
                                       kwargs={
                                           'rulebook_slug': rulebook.slug,
                                           'rulebook_id': rulebook_id, })

    feat_list = rulebook.feat_set.select_related('rulebook',
                                                 'rulebook__dnd_edition').all()

    paginator = DndMobilePaginator(feat_list, request)

    return render_to_response('dnd/mobile/feats/feats_in_rulebook.html',
                              {
                                  'rulebook': rulebook,
                                  'feat_list': paginator.items(),
                                  'paginator': paginator,
                                  'request': request,
                                  'display_3e_warning': is_3e_edition(rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )


@menu_item("feats")
@submenu_item("feats")
def feat_detail_mobile(request, rulebook_slug, rulebook_id, feat_slug, feat_id):
    feat = get_object_or_404(
        Feat.objects.select_related('rulebook', 'rulebook__dnd_edition'),
        pk=feat_id)
    if (feat.slug != feat_slug or
                unicode(feat.rulebook.id) != rulebook_id or
                feat.rulebook.slug != rulebook_slug):
        return permanent_redirect_object_mobile(request, feat)

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

    return render_to_response('dnd/mobile/feats/feat_detail.html',
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

