# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from dndtools.dnd.urls import desktop_to_mobile


class MobileMiddleware(object):
    @staticmethod
    def is_mobile():
        return True

    @staticmethod
    def is_forced_desktop(request):
        return request.COOKIES.get('force_desktop', False)

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

        ## mobile version is not required
        #if not self.is_mobile() or self.is_forced_desktop(request):
        #    return None
        #
        ## is there a mobile version of this page?
        #if view_func.func_name in desktop_to_mobile:
        #    url = reverse(desktop_to_mobile[view_func.func_name], args=view_args, kwargs=view_kwargs)
        #    # get parameters
        #    if len(request.GET) > 0:
        #        #noinspection PyUnresolvedReferences
        #        url += "?" + request.GET.urlencode()
        #
        #    return HttpResponseRedirect(url)