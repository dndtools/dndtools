# -*- coding: utf-8 -*-
from django.contrib.admin.models import LogEntry

from django.contrib.syndication.views import Feed


class AdminLogFeed(Feed):
    title = "DnDTools.eu changes"
    link = ''
    description = "What our great admins are working on right now."

    def items(self):
        log_list = LogEntry.objects.filter(
            content_type__app_label='dnd').order_by('-action_time').all()[:50]

        result = []

        for entry in log_list:
            if False:
                entry = LogEntry()

            change_message = entry.change_message
            url = None
            object_rep = entry.object_repr
            try:
                obj = entry.get_edited_object()
                object_rep = obj.__unicode__()
                url = obj.get_absolute_url()
            except Exception:
                pass

            result.append({
                'object_rep': object_rep,
                'change_message': change_message,
                'url': url,
                'is_addition': entry.is_addition(),
                'is_change': entry.is_change(),
                'is_deletion': entry.is_deletion(),
                'author': entry.user,
                'pub_date': entry.action_time
            })

        return result

    def item_title(self, item):
        if item['is_change']:
            return 'Changed %s' % item['object_rep']
        elif item['is_addition']:
            return 'Added %s' % item['object_rep']
        else:
            return 'Deleted %s' % item['object_rep']

    def item_description(self, item):
        if item['is_change']:
            base =  '%s -- %s' % (item['object_rep'], item['change_message'])
        elif item['is_addition']:
            base = 'Added %s' % item['object_rep']
        else:
            base = 'Deleted %s' % item['object_rep']

        return "%s<br/><br/>(%s)" % (base, item['author'].first_name)

    def item_author_name(self, item):
        return item['author'].first_name

    def item_link(self, item):
        if item['url']:
            return item['url']
        return ''

    def item_pubdate(self, item):
        return item['pub_date']
