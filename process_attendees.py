

with open('attendees.html') as in_file:
    attendees = []
    attendees_by_name = {}
    current = {}

    info_count = 0
    for line in in_file:
        if '<h3>' in line:
            current['name'] = line[4:-6]

        if '<img' in line:
            out = line.split('src=')
            current['image'] = out[1][1:-3]

        if 'attendee-info' in line:
            info_count += 1
            out = line[27:-7]
            if out.endswith(','):
                out = out[:-1]
            current['info' + str(info_count)] = out


        if 'attendee-country' in line:
            info_count = 0
            current['country'] = line[30:-7]
            attendees.append(current)

            attendees_by_name[current['name']] = current

            current = {}

import json

out_file = open('attendees.json', 'w+')
out_file.write(json.dumps(attendees, sort_keys=True, indent=2, separators=(',', ': ')))
out_file.close()

out_file1 = open('attendees_by_name.json', 'w+')
out_file1.write(json.dumps(attendees_by_name, sort_keys=True, indent=2, separators=(',', ': ')))
out_file1.close()

print len(attendees)
print len(attendees_by_name.items())
