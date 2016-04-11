# -*- coding: utf-8 -*-
"""
Created on Tue May 19 11:55:23 2015

@author: SSunshine
"""
#!/usr/bin/env python
""" Countdown Timer

Basic countdown timer script that takes a date(time) input and actively
counts down until that moment in time.
"""

# Standard Library Imports
import sys
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from datetime import datetime
from time import sleep
#from time import ctime
import ntplib


TIME_SERVER = 'pool.ntp.org'


def _mkdatetime(datestr):
    """
    Datetime argument parser
    Deconstructs a (partial) datetime representation into the native
    python datetime type

    @param datestr: str, datetime-like ISOformat-like representation of
        a date
    @return: datetime
    """
    try:
        return datetime(*map(int, datestr.split('-')))
    except ValueError:
        raise ArgumentTypeError(datestr + ' is not a proper date string')


def date_back(dt, from_date=None, precise=False):
    """
    Provides a human readable format for a timedelta

    @param dt: datetime, this is time equal or older than now or the
        date in 'from_date'
    @param from_date: datetime, when None the 'now' is used otherwise a
        concrete date is expected
    @param precise: Bool, when true then milliseconds and microseconds
        are included
    @return: str, timedelta as human readable string
    """
    if not from_date:
#        from_date = datetime.now()
        c = ntplib.NTPClient()
       # response = c.request(TIME_SERVER)
         
        tries = 0
        response = None
        while not response and tries <= 3:
            tries += 1
            try:
                response = c.request(TIME_SERVER)
            except Exception:
                print("Error with the time server...")
        
        if response is None:
            raise Exception("Fatal error communicating with the time server")
                
        from_date = datetime.fromtimestamp(response.tx_time)

    if dt < from_date:
        return None
    elif dt == from_date:
        return "now"

    delta = dt - from_date

    deltaMinutes = delta.seconds // 60
    deltaHours = delta.seconds // 3600
    deltaMinutes -= deltaHours * 60
    deltaWeeks = delta.days    // 7
    deltaSeconds = delta.seconds - deltaMinutes * 60 - deltaHours * 3600
    deltaDays = delta.days    - deltaWeeks * 7
    deltaMilliSeconds = delta.microseconds // 1000
    deltaMicroSeconds = delta.microseconds - deltaMilliSeconds * 1000

    valuesAndNames = [
        (deltaWeeks, "week"),
        (deltaDays, "day"),
        (deltaHours, "hour"),
        (deltaMinutes, "minute"),
        (deltaSeconds, "second")
    ]
    if precise:
        valuesAndNames.append((deltaMilliSeconds, "millisecond"))
        valuesAndNames.append((deltaMicroSeconds, "microsecond"))

    text =""
    for value, name in valuesAndNames:
        if value > 0:
            text += len(text)   and ", " or ""
            text += "%d %s" % (value, name)
            text += (value > 1) and "s" or ""

    # replacing last occurrence of a comma by an 'and'
    if text.find(",") > 0:
        text = " and ".join(text.rsplit(", ",1))

    return text


def countdown(dt, subject=None):
    """
    Countdown timer

    @param dt: datetime to countdown to
    @param subject: str|None, the name of the subject to which we are
        counting down to
    """

    delta_str = date_back(dt)
    while delta_str:
        sys.stdout.flush()
        delta_str = date_back(dt)
        message = "Time left{until}: {datetime}\r".format(
            until=" until {0}".format(subject) if subject else "",
            datetime=delta_str
        )
        sys.stdout.write(message)
        sleep(0.1)


def main():
    """
    Main program entry
    """
    argparser = ArgumentParser(description="Basic countdown timer.")
    argparser.add_argument("target_datetime", type=_mkdatetime)
    argparser.add_argument("--subject", type=str, required=False)
    args = argparser.parse_args()

    try:
        countdown(args.target_datetime, args.subject)
        print("*"*80)
        print("THE TIME IS NOW!")
        print("*"*80)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
