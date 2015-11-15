from django.views import generic

from attendees.models import Concept, Attendee

import json


class AttendeesView(generic.TemplateView):
    template_name = 'attendees/index.html'

    def get_context_data(self, *args, **kwargs):
        data = super(AttendeesView, self).get_context_data(*args, **kwargs)
        data['concepts_json'] = json.dumps(list(
            Concept.objects.values_list('label', flat=True).distinct()))
        return data


class AttendeesAjaxView(generic.TemplateView):
    template_name = 'attendees/partial.html'

    def get_context_data(self, *args, **kwargs):
        data = super(AttendeesAjaxView, self).get_context_data(*args, **kwargs)
        tags_str = self.request.GET.get('tags', '')
        if tags_str:
            tags = tags_str.split(',')
            data['results'] = Attendee.objects.filter(concepts__label__in=tags).distinct()
        return data
