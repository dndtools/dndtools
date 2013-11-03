# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from dndtools.dnd.models import Rule
from dndtools.dnd.views import is_3e_edition


def rule_detail_mobile(request, rule_id):
    rule = get_object_or_404(
        Rule.objects.select_related('rulebook', 'rulebook__dnd_edition'),
        pk=rule_id)

    return render_to_response('dnd/mobile/rules/rule_detail.html',
                              {
                                  'rule': rule,
                                  'rulebook': rule.rulebook,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(rule.rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )