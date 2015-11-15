from django.views import generic
from django.db.models import Count

from attendees.models import Concept, Attendee

import json


class AttendeesView(generic.TemplateView):
    template_name = 'attendees/index.html'

    def get_context_data(self, *args, **kwargs):
        data = super(AttendeesView, self).get_context_data(*args, **kwargs)
        data['top_labels'] = Concept.objects.exclude(
            label__in=['', 'LinkedIn']
        ).values('label').annotate(count=Count('label')).order_by('-count')[:7]
        data['random_labels'] = Concept.objects.values('label').random(7)
        all_labels = Concept.objects.values_list('label', flat=True).distinct()
        data['all_labels_select2_data'] = json.dumps([{
            'id': l,
            'text': l
        } for l in all_labels])
        Concept.objects.values('label').annotate(count=Count('label'))
        return data


class AttendeesAjaxView(generic.TemplateView):
    template_name = 'attendees/partial.html'

    def get_context_data(self, *args, **kwargs):
        data = super(AttendeesAjaxView, self).get_context_data(*args, **kwargs)
        tags_str = self.request.GET.get('tags', '')
        if tags_str:
            tags = tags_str.split(',')
            data['tags'] = ','.join(tags)
            data['results'] = list(Attendee.objects.filter(concepts__label__in=tags).distinct())
            data['results_len'] = len(data['results'])
        return data
