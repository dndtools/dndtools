# -*- coding: utf-8 -*-

from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from reversion.revisions import revision
from dndtools.dnd.menu import menu_item, submenu_item, MenuItem
from dndtools.dnd.forms import InaccurateContentForm
from dndtools.dnd.models import NewsEntry


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


def is_admin(request):
    return request.user.is_staff and request.user.is_active


@menu_item(MenuItem.CONTACTS)
@submenu_item(MenuItem.Contacts.NEWS)
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


