# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from dnd.dnd_paginator import DndPaginator
from dnd.filters import RuleFilter
from dnd.menu import menu_item, MenuItem, submenu_item
from dnd.views import permanent_redirect_object
from dnd.models import Rule
from dnd.views import is_3e_edition


@menu_item(MenuItem.RULEBOOKS)
@submenu_item(MenuItem.Rulebooks.RULES)
def rule_list(request):
    f = RuleFilter(request.GET, queryset=Rule.objects.all())

    form_submitted = 1 if '_filter' in request.GET else 0

    paginator = DndPaginator(f.qs, request)

    return render_to_response('dnd/rules/rule_list.html',
                              {
                                  'request': request,
                                  'rule_list': paginator.items(),
                                  'paginator': paginator,
                                  'filter': f,
                                  'form_submitted': form_submitted,
                              }, context_instance=RequestContext(request), )


@menu_item(MenuItem.RULEBOOKS)
@submenu_item(MenuItem.Rulebooks.RULES)
def rule_detail(request, rulebook_slug, rulebook_id, rule_slug, rule_id):
    rule = get_object_or_404(
        Rule.objects.select_related('rulebook', 'rulebook__dnd_edition'),
        pk=rule_id)
    if (rule.slug != rule_slug or
                unicode(rule.rulebook.id) != rulebook_id or
                rule.rulebook.slug != rulebook_slug):
        return permanent_redirect_object(request, rule)

    return render_to_response('dnd/rules/rule_detail.html',
                              {
                                  'rule': rule,
                                  'rulebook': rule.rulebook,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(rule.rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )
