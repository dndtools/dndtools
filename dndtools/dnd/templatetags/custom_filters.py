# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from dndtools import settings
import locale
from dndtools.dnd.utilities import int_with_commas


register = template.Library()

BOOLEAN_MAPPING = {True: 'yes', False: 'no', None: 'unknown', 1: 'yes',
                   0: 'no', '1': 'yes', '0': 'no', u'1': 'yes'}
def _boolean_as_img(value):
    try:
        mapped = BOOLEAN_MAPPING[value]
    except Exception:
        mapped = BOOLEAN_MAPPING[None]

    return mark_safe(u'<img src="%simg/admin/icon-%s.gif" alt="%s" class="yes-no-icon" />' % (
        settings.ADMIN_MEDIA_PREFIX, mapped, mapped))
_boolean_as_img.is_safe = False

def _plus_minus(value):
    try:
        i = int(value)

        if i >= 0:
            return '+%d' % i
        else:
            return mark_safe(u'&minus;%d' % (-i))
    except Exception:
        return value

def _empty_as_dash(value):
    if value:
        return value
    return mark_safe(u'&mdash;')

def _ordinal_number(value):
    if not value:
        return value

    if not isinstance(value, int):
        return value

    if value == 11:
        return '%d%s' % (value, 'th')
    if value % 10 == 1:
        return '%d%s' % (value, 'st')
    if value % 10 == 2:
        return '%d%s' % (value, 'nd')
    if value % 10 == 3:
        return '%d%s' % (value, 'rd')

    return '%d%s' % (value, 'th')

def _thousands_separator(value):
    return int_with_commas(value)

register.filter('boolean_as_img', _boolean_as_img)
register.filter('plus_minus', _plus_minus)
register.filter('empty_as_dash', _empty_as_dash)
register.filter('ordinal_number', _ordinal_number)
register.filter('thousands_separator', _thousands_separator)