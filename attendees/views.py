from django.views import generic
from django.http import HttpResponse
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count

from attendees.models import Concept, Attendee
from attendees.todoist import export_to_todoist

import json
import operator


class AttendeesView(generic.TemplateView):
    template_name = 'attendees/index.html'

    def get_context_data(self, *args, **kwargs):
        data = super(AttendeesView, self).get_context_data(*args, **kwargs)
        data['top_labels'] = Concept.objects.exclude(
            label__in=['', 'LinkedIn']
        ).values('label').annotate(count=Count('label')).order_by('-count')[:7]
        data['random_labels'] = Concept.objects.values('label').random(7)
        return data


def filter_query(tags):
    return Attendee.objects.filter(
        concepts__label__in=tags).annotate(
        count=Count('concepts')).filter(count=len(tags))


class SendToTodoistAjaxView(generic.TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SendToTodoistAjaxView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        tags_str = self.request.POST.get('tags', '')
        tags = tags_str.split(',')
        attendees = filter_query(tags)
        if len(attendees) >= 20:
            attendees = attendees[:20]
        print attendees
        export_to_todoist(username, password, 'TheNextWeb-networking', attendees)
        return HttpResponse()


class AttendeesAjaxView(generic.TemplateView):
    template_name = 'attendees/partial.html'

    def get_context_data(self, *args, **kwargs):
        data = super(AttendeesAjaxView, self).get_context_data(*args, **kwargs)
        tags_str = self.request.GET.get('tags', '')
        if tags_str:
            tags = tags_str.split(',')

            attendees_full = list(filter_query(tags))
            attendees = attendees_full
            if len(attendees) > 30:
                attendees = attendees[:30]

            data['tags'] = ', '.join(tags)
            data['results'] = attendees
            data['results_len'] = len(attendees_full)
        return data

class ConceptsFilterEndpoint(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        p = request.GET.get('term')
        concepts = Concept.objects.filter(label__contains=p).values_list('label', flat=True).distinct()[:10]
        return HttpResponse(json.dumps([{
            'id': l,
            'text': l
        } for l in concepts]))
