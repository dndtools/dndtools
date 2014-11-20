# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template.context import Context

from dnd.dnd_paginator import DndPaginator


class DndMobilePaginator(DndPaginator):
    def print_navigation(self):
        template = get_template('dnd/mobile/dndpaginator_navigation.html')
        context = Context({
            'page_obj': self.page,
            'pages': self.pages,
            'available_page_sizes': self.available_page_sizes,
            'selected_page_size': self.page_size,
            'count': self.count(),
            'get_vars': self.get_vars,
            'get_vars_solo': self.get_vars_solo(),
            'hidden_inputs': self.hidden_inputs,
        })
        return template.render(context)