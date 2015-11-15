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
        all_labels = Concept.objects.values_list('label', flat=True).distinct()
        data['all_labels_select2_data'] = json.dumps([{
            'id': l,
            'text': l
        } for l in all_labels])
        Concept.objects.values('label').annotate(count=Count('label'))
        return data


def filter_query(tags):
    # concepts = Concept.objects.filter(label__in=tags).annotate(count=Count('attendee'))
    # print concepts[0].count
    return Attendee.objects.filter(concepts__label__in=tags).annotate(count=Count('concepts')).filter(count=len(tags))

    return Attendee.objects.filter(
        reduce(operator.and_, (Q(concepts__label=t) for t in tags))
    ).distinct()


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
            data['tags'] = ', '.join(tags)
            data['results'] = list(filter_query(tags))
            data['results_len'] = len(data['results'])
        return data
