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
    filename = os.path.join(HOME, 'log')
    now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))

    if not msg:
        # read mode
        with open(filename, 'r') as f:
            # TODO optimize me!
            # print lines from today
            for line in f:
                if line.startswith(now.isoformat()[:10]):
                    print(line.strip())
    else:
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
                    timediff = '+{:02d}:{:02d}'.format(hours, minutes)
        except FileNotFoundError:
            timediff = ''

        # write new line
        with open(filename, 'a') as f:
            f.write('{} ({}): {}\n'.format(now.isoformat(), timediff, msg))

