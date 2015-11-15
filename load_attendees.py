import json

from attendees.models import Attendee
from attendees.concept_insights import fetch_concepts

a_file = open('final.json')

attendees = json.loads(a_file.read())

for attendee in attendees:
    if attendee['link']:
        attendee_instance, new = Attendee.objects.get_or_create(name=attendee['name'],
            defaults={
                'company': attendee['company'],
                'picture': attendee['image'],
                'linkedin_profile': attendee['link']})

        print 'created: ' + attendee_instance.name

        if new:
            fetch_concepts(attendee_instance, html=attendee['html'])

