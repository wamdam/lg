#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Usage:
    lg
    lg -a
    lg <message>
"""

import sys
import datetime
import dateutil.parser
import pytz
import os
HOME = os.path.expanduser("~")
filename = os.path.join(HOME, 'log')

def read_line(line):
    """ Reads a line in this format:
        2015-07-08 18:26:27+02:00: Weltbild display none Problem Analyse
        and returns a tuple of datetime and message.
    """
    datestr, message = line.split(': ', 1)
    last_datetime = dateutil.parser.parse(datestr)
    return last_datetime, message


def calc_diff(last, cur):
    """ Calculates the difference in days, hours, minutes and seconds between last and cur
    """
    difference = cur - last
    minutes, seconds = divmod(difference.days * 86400 + difference.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes, seconds)


def format(cur, days, hours, minutes, msg):
    """ Formats a line for output.
        last and cur are datetime, msg is str
    """
    if days:
        timediff = '+{} days'.format(days)
    else:
        timediff = '+{:02d}:{:02d}'.format(hours, minutes)
    #return '{} ({}): {}'.format(cur.strftime('%Y-%m-%d %H:%M:%S'), timediff, msg.strip())
    return '{} ({}): {}'.format(cur.strftime('%H:%M:%S'), timediff, msg.strip())


def show(lines):
    """ returns a list of formatted lines for a day. Also provides
    a sum of work- and slacking time
    """
    ret = []
    last = None
    sum_minutes = 0.0
    sum_minutes_slack = 0.0
    for line in lines:
        cur, msg = read_line(line)
        if not last:
            last = cur
            ret.append(cur.date().strftime('%Y-%m-%d'))
            ret.append('='*78)
        days, hours, minutes, seconds = calc_diff(last, cur)
        if '**' in msg:
            sum_minutes_slack += 1440*days + 60*hours + minutes + seconds/60
        else:
            sum_minutes += 1440*days + 60*hours + minutes + seconds/60
        ret.append(format(cur, days, hours, minutes, msg))
        last = cur

    ret.append('          ------')
    ret.append('           {:02d}:{:02d} (+{:02d}:{:02d} slacking)'.format(
        int(sum_minutes)//60, round(sum_minutes)%60,
        int(sum_minutes_slack)//60, round(sum_minutes_slack)%60
    ))
    ret.append('')
    sum_minutes = 0.0
    sum_minutes_slack = 0.0
    return ret


if __name__ == '__main__':
    msg = " ".join(sys.argv[1:])
    now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))

    if not msg:
        # read mode
        today = now.strftime('%Y-%m-%d')
        lines = []
        with open(filename, 'r') as f:
            # print lines from today
            for line in f:
                if line.startswith(today):
                    lines.append(line)
            print('\n'.join(show(lines)))

    elif msg == '-a':
        lines = []
        last_day = None
        with open(filename, 'r') as f:
            for line in f:
                cur_day = line[:10]
                if not last_day:
                    last_day = cur_day
                if last_day != cur_day:
                    print('\n'.join(show(lines)))
                    lines = []
                    last_day = cur_day
                lines.append(line)
            print('\n'.join(show(lines)))

    else:
        # write new line
        with open(filename, 'a') as f:
            f.write('{}: {}\n'.format(now.strftime('%Y-%m-%d %H:%M:%S%z'), msg))

