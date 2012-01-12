# -*- coding: UTF-8 -*-

"""
reads file (name given as call parameter) of following format:
header
(room number, whatever, capacity, (whatever,)*)*
prints json to standard output
"""

import datetime
import sys

print '[',

id_start = 100

try:
    file = open( sys.argv[1], mode='r', )
    for line in file.readlines()[1:-1]:
        try:
            room = line.split(',')
            print "{\"pk\": " + str(id_start) + ", \"model\": \"newrooms.nroom\", \"fields\": {\"short_unlock_time\": \"" + \
                                         str(datetime.datetime.now()) + "\", \"capacity\": " + str(room[2]) + ", \"number\": \"" + str(room[0]) + "\"}}, "
            id_start += 1
        except IndexError:
            pass
except IndexError:
    print "type: python get_corp.py filename_in filename_out"

print ' ]'