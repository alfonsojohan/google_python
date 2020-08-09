#!/usr/bin/env python3

import operator
import re
import csv

h = open('syslog.log')

error = {}
per_user = {}

patterns = (r'ticky: ERROR', r'ticky: INFO')

for l in h:
    l = l.rstrip()
    if re.search(patterns[0], l):
        r = re.search(r"ERROR ([\w' ]*) ([().\w]+)", l)
        error[r.group(1)] = error.get(r.group(1), 0) + 1
        name = r.group(2).replace('(', '').replace(')', '')
        if name not in per_user.keys(): per_user[name] = {'error': 0, 'info': 0}
        per_user[name]['error'] = per_user[name]['error'] + 1
    elif re.search(patterns[1], l):
        r = re.search(r"([().\w]+)$", l)
        name = r.group(1).replace('(', '').replace(')', '')
        if name not in per_user.keys(): per_user[name] = {'error': 0, 'info': 0}
        per_user[name]['info'] = per_user[name]['info'] + 1
h.close()

error = sorted(error.items(), key=operator.itemgetter(1), reverse=True)
user = sorted(per_user.items())

h = open('error_message.csv', 'w+', newline='')
csv_out = csv.writer(h)
csv_out.writerow(('Error', 'Count'))
for l in error:
    csv_out.writerow(l)
h.close()

h = open('user_statistics.csv', 'w+', newline='')
csv_out = csv.writer(h)
csv_out.writerow(('Username', 'INFO', 'ERROR'))
for u, t in user:
    row = (u, t['info'], t['error'])
    csv_out.writerow(row)
h.close()