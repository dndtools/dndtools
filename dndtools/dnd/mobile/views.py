# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect


def force_desktop_version(request):
    response = HttpResponseRedirect(request.GET.get('back_url'))
    response.set_cookie('force_desktop', True)
    return response