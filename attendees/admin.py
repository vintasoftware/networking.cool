from django.contrib import admin

from attendees.models import Attendee, Concept


class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ConceptAdmin(admin.ModelAdmin):
    list_display = ('label', 'attendee', 'score',)
    list_filter = ('label', 'attendee',)



admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Concept, ConceptAdmin)
