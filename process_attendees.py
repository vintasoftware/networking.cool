

with open('attendees.json', 'w+') as out_file:
    with open('attendees.html') as in_file:
        out_file.write('[')

        info_count = 0
        for line in in_file:
            if '<h3>' in line:
                out_file.write('{"name": "' + line[4:-6] + '",')
                out_file.write('\n')

            if 'attendee-info' in line:
                info_count += 1
                out = line[27:-7]
                if out.endswith(','):
                    out = out[:-1]
                out_file.write('"info' + str(info_count) + '": "' + out + '",')
                out_file.write('\n')

            if 'attendee-country' in line:
                out_file.write('"country": "' + line[30:-7] + '"},')
                out_file.write('\n')
                out_file.write('\n')
                info_count = 0

        out_file.write(']')


