

with open('attendees.json', 'w+') as out_file:
    with open('attendees.html') as in_file:

        attendees = []

        current = {}

        # out_file.write('[')

        info_count = 0
        for line in in_file:
            if '<h3>' in line:
                current['name'] = line[4:-6]
                # out_file.write('{"name": "' + line[4:-6] + '",')
                # out_file.write('\n')

            if '<img' in line:
                out = line.split('src=')
                current['image'] = out[1][1:-3]
                # out_file.write('"image": ' + out[1] + '",')

            if 'attendee-info' in line:
                info_count += 1
                out = line[27:-7]
                if out.endswith(','):
                    out = out[:-1]
                current['info' + str(info_count)] = out

                # out_file.write('"info' + str(info_count) + '": "' + out + '",')
                # out_file.write('\n')

            if 'attendee-country' in line:
                # out_file.write('"country": "' + line[30:-7] + '"},')
                # out_file.write('\n')
                # out_file.write('\n')
                info_count = 0
                current['country'] = line[30:-7]
                attendees.append(current)

                current = {}

        # out_file.write(']')


    import json
    out_file.write(json.dumps(attendees, sort_keys=True, indent=2, separators=(',', ': ')))

