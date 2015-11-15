
import json

res = open('results.json')
by_name_file = open('attendees_by_name.json')

attendees = json.loads(res.read())
by_name = json.loads(by_name_file.read())

for attendee in attendees:
    attendee['image'] = by_name[attendee['name']]['image']


res.close()


res = open('final.json', 'w+')
res.write(json.dumps(attendees, sort_keys=True, indent=2, separators=(',', ': ')))
