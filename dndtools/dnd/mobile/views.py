# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect


def permanent_redirect_object_mobile(request, object):
    url = object.get_absolute_url_mobile()
    # get parameters
    if len(request.GET) > 0:
        #noinspection PyUnresolvedReferences
        url += "?" + request.GET.urlencode()

    return HttpResponsePermanentRedirect(url)


def force_desktop_version(request):
    url = request.GET.get('back_url')
    if not url:
        url = reverse('index')
    response = HttpResponseRedirect(url)
    response.set_cookie('force_desktop', True)
    return response


def return_to_mobile_version(request):
    url = request.META.get('HTTP_REFERER')
    if not url:
        url = reverse('index')
    response = HttpResponseRedirect(url)
    response.delete_cookie('force_desktop')
    return response