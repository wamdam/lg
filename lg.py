#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Usage:
    lg <message>
"""

import sys
import datetime
import dateutil.parser
import pytz
import os
HOME = os.path.expanduser("~")

if __name__ == '__main__':
    msg = " ".join(sys.argv[1:])
    now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))

    filename = os.path.join(HOME, 'log')

    # get last line and parse date
    try:
        with open(filename, 'rb') as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(-size, -1024), 2)
            last = f.readlines()[-1].decode()
            last_datetime = dateutil.parser.parse(last.split()[0])
            difference = now - last_datetime
            minutes, seconds = divmod(difference.days * 86400 + difference.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            if days:
                timediff = '+{} days'.format(days)
            else:
                timediff = '+{0:02d}:{0:02d}'.format(hours, minutes)
    except FileNotFoundError:
        timediff = ''

    # write new line
    with open(filename, 'a') as f:
        f.write('{} ({}): {}\n'.format(now.isoformat(), timediff, msg))

