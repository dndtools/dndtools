# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from dnd.mobile.views import permanent_redirect_object_mobile
from dnd.models import Rule
from dnd.views import is_3e_edition


def rule_detail_mobile(request, rulebook_slug, rulebook_id, rule_slug, rule_id):
    rule = get_object_or_404(
        Rule.objects.select_related('rulebook', 'rulebook__dnd_edition'),
        pk=rule_id)
    if (rule.slug != rule_slug or
                unicode(rule.rulebook.id) != rulebook_id or
                rule.rulebook.slug != rulebook_slug):
        return permanent_redirect_object_mobile(request, rule)

    return render_to_response('dnd/mobile/rules/rule_detail.html',
                              {
                                  'rule': rule,
                                  'rulebook': rule.rulebook,
                                  'request': request,
                                  'i_like_it_url': request.build_absolute_uri(),
                                  'inaccurate_url': request.build_absolute_uri(),
                                  'display_3e_warning': is_3e_edition(rule.rulebook.dnd_edition),
                              }, context_instance=RequestContext(request), )