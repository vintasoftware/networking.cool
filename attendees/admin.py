from django.contrib import admin

from attendees.models import Atendee, Concept


class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ConceptAdmin(admin.ModelAdmin):
    list_display = ('label', 'atendee', 'score',)
    list_filter = ('label', 'atendee',)



admin.site.register(Atendee, AttendeeAdmin)
admin.site.register(Concept, ConceptAdmin)
