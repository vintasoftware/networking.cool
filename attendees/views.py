from django.shortcuts import render
from django.views import generic


class AttendeesView(generic.TemplateView):
    template_name = 'attendees/index.html'
