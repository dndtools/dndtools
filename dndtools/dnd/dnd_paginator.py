# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import exceptions
from django.template.context import Context
from django.template.loader import get_template


class DndPaginator():
    available_page_sizes = (20, 50, 100, 1000)

    def __init__(self, qs, request):
        self.qs = qs
        self.request = request

        self.page_size = request.session.get('page_size',
            self.available_page_sizes[0])

        # overwrite with new value, if it is correct
        if 'page_size' in request.GET:
            try:
                ps = int(request.GET['page_size'])
                if ps in self.available_page_sizes:
                    self.page_size = ps
                    request.session['page_size'] = ps
            except exceptions.ValueError:
                pass

        try:
            self.page_number = int(request.GET.get('page', '1'))
        except ValueError:
            self.page_number = 1

        self.paginator = Paginator(self.qs, self.page_size)

        try:
            self.page = self.paginator.page(self.page_number)
        except (EmptyPage, InvalidPage):
            self.page = self.paginator.page(self.paginator.num_pages)

        # calculate pages
        self.pages = []

        add_none = True
        for page in self.paginator.page_range:
            if (page < 3
                or self.paginator.num_pages - page < 3
                or abs(page - self.page.number) < 3):
                add_none = True
                self.pages.append(page)
            elif add_none:
                self.pages.append(None)
                add_none = False

        # create get_vars
        get_vars = request.GET.copy()
        if 'page' in get_vars:
            del get_vars['page']
        if len(get_vars.keys()) > 0:
            self.get_vars = "&%s" % get_vars.urlencode()
        else:
            self.get_vars = ''
        if 'page_size' in get_vars:
            del get_vars['page_size']
        self.hidden_inputs = get_vars.items()

    def print_navigation(self):
        template = get_template('dnd/dndpaginator_navigation.html')
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

    def print_rel_prev_next(self):
        template = get_template('dnd/dndpaginator_rel_prev_next.html')
        context = Context({
            'page_obj': self.page,
            'get_vars': self.get_vars,
            'get_vars_solo': self.get_vars_solo(),
            })
        return template.render(context)

    def items(self):
        return self.page.object_list

    def count(self):
        return self.paginator.count

    def num_pages(self):
        return self.paginator.num_pages

    def get_vars_solo(self):
        if self.get_vars == '':
            return '.'

        return '?' + self.get_vars[1:]