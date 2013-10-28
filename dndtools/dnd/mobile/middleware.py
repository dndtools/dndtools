# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from dnd.mobile.mobile_dispatcher import MobileDispatcher


class MobileMiddleware(object):
    BETA_VERSION_NO_MOBILE = True

    def __init__(self):
        self.mobile_dispatcher = MobileDispatcher()

    @staticmethod
    def is_mobile():
        return True

    @staticmethod
    def is_forced_desktop(request):
        return 'force_desktop' in request.COOKIES

    def process_view(self, request, view_func, view_args, view_kwargs):
        if self.BETA_VERSION_NO_MOBILE:
            return None

        is_mobile = self.is_mobile()
        request.is_mobile = is_mobile

        # mobile version is not required
        if not is_mobile or self.is_forced_desktop(request):
            return None

        dispatch_url = self.mobile_dispatcher.dispatch(view_func.func_name, view_args, view_kwargs)
        if dispatch_url:
            if len(request.GET) > 0:
                #noinspection PyUnresolvedReferences
                dispatch_url += "?" + request.GET.urlencode()

            return HttpResponseRedirect(dispatch_url)