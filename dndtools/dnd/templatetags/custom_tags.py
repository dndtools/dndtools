# -*- coding: utf-8 -*-
import os
import urlparse
from django import template
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
import dndproject.settings


register = template.Library()


class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])


def _absolute_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return url
    domain = Site.objects.get_current().domain
    return 'http://%s%s' % (domain, url)


@register.simple_tag
def static(filename, flags=''):
    """
        see http://insist.sk/blog/django/149.html
    """
    flags = set(f.strip() for f in flags.split(','))
    url = urlparse.urljoin(dndproject.settings.STATIC_URL, filename)
    if 'absolute' in flags:
        url = _absolute_url(url)
    if (filename.endswith('.css') or filename.endswith('.js')) and 'no-timestamp' not in flags or \
       'timestamp' in flags:
        fullname = os.path.join(dndproject.settings.STATICFILES_DIRS[0], filename)
        if os.path.exists(fullname):
            url += '?%d' % os.path.getmtime(fullname)
    return url


@register.simple_tag
def media(filename, flags=''):
    """
        see http://insist.sk/blog/django/149.html
    """
    flags = set(f.strip() for f in flags.split(','))
    url = urlparse.urljoin(dndproject.settings.MEDIA_URL, filename)
    if 'absolute' in flags:
        url = _absolute_url(url)
    if (filename.endswith('.css') or filename.endswith('.js')) and 'no-timestamp' not in flags or \
       'timestamp' in flags:
        fullname = os.path.join(dndproject.settings.MEDIA_ROOT, filename)
        if os.path.exists(fullname):
            url += '?%d' % os.path.getmtime(fullname)
    return url

register.tag('set', set_var)