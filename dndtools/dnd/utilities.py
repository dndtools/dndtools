# -*- coding: utf-8 -*-
import re
from django.utils.html import escape
import textile


def remove_special_chars(s, strict=False):
    if not strict:
        s = re.sub(r'fl +(?=[A-z])', 'fl', s)
        s = re.sub(r'fj +(?=[A-z])', 'fj', s)
        s = re.sub(r'fi +(?=[A-z])', 'fi', s)
    s = re.sub(u'ﬁ *', 'fi', s)
    s = re.sub(u'ﬂ *', 'fl', s)
    s = re.sub(u'’', "'", s)
    s = re.sub(u'[–—]', "--", s)
    s = re.sub(u'[“”]', '"', s)
    return s


def create_links(s):
    """
    Creates HTML links from format

    &quote;link title&quote;:feats/lords-of-madness--72/aberration-blood--8/
    &quote;link title&quote;:/feats/lords-of-madness--72/aberration-blood--8/

    The usage of "&quote;" instead of quote character itself is because text is escaped first and only then it is textilized.

    wont create link that has anything other than A-z0-9, "(", ")", ":" or space in their name and wont allow for absolute URLs (eg. http://foo.bar)
    """
    return re.sub(r"&quot;((?:[-\w ():/]|&#39;)+)&quot;:/?(?![-a-z0-9/]+://)([-a-z0-9/]+)", r'<a href="/\2">\1</a>', s)


def create_hr(s):
    """
    Replaces ----- (five or more dashes) into <hr/>
    """
    return re.sub(u'-{5,}', '<hr/>', s)


def update_html_cache_attributes(object, *args):
    for attr_name in args:
        value = getattr(object, attr_name)

        # remove ligatures and other bad characters
        value = remove_special_chars(value, strict=True)
        # set it back to the object
        setattr(object, attr_name, value)

        # apply textile
        value = escape(value)
        value = create_hr(value)
        value = create_links(value)

        value = textile.textile(value)
        value = re.sub(r'\[errata\](.*?)\[new\](.*?)\[/errata\]',
                       r'<span class="errata-old">\1</span><span class="errata-new">\2</span>', value)

        # set it to '_html'
        setattr(object, '%s_html' % attr_name, value)


def int_with_commas(x):
    if type(x) == (type(0.0)):
        x = int(x)
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer, got %s" % type(x).__name__)
    if x < 0:
        return '-' + int_with_commas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)