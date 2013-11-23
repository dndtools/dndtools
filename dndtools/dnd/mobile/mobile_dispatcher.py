# -*- coding: utf-8 -*-
import re

from django.core.urlresolvers import reverse


class MobileDispatcher(object):
    def __init__(self):
        # TODO autodispatch
        self.dispatch_methods = {}

        for method_name in dir(self):
            m = re.match(r'^_dispatch_(.*)$', method_name)
            if m:
                dispatch_method = getattr(self, method_name)

                if hasattr(dispatch_method, '__call__'):
                    self.dispatch_methods[m.group(1)] = dispatch_method

        pass

    def dispatch(self, view_func_name, args, kwargs):
        if view_func_name in self.dispatch_methods:
            return self.dispatch_methods[view_func_name](args, kwargs)

        return None

    @staticmethod
    def _dispatch_feat_index(args, kwargs):
        return reverse('feat_index_mobile')

    @staticmethod
    def _dispatch_feat_category_list(args, kwargs):
        return reverse('feat_detail_mobile')

    @staticmethod
    def _dispatch_feat_category_detail(args, kwargs):
        return reverse('feat_category_detail_mobile', kwargs=kwargs)

    @staticmethod
    def _dispatch_feats_in_rulebook(args, kwargs):
        return reverse('feats_in_rulebook_mobile', kwargs={'rulebook_id': kwargs['rulebook_id']})

    @staticmethod
    def _dispatch_feat_detail(args, kwargs):
        return reverse('feat_detail_mobile', kwargs={'feat_id': kwargs['feat_id']})