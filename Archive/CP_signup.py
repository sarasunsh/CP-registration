#!/usr/bin/env python
"""
"""

# Third Party Library Imports
import requests
from datetime import date
from datetime import datetime
from datetime import time

# Local Package Imports
from countdown import countdown

URL = "https://classpass.com/a/PassportReserveDialog"

def CP_send(sched_id, venue_id, class_id, class_name, COOKIES): 

    class_payload =  {
        'schedule_id': sched_id, 
        'class_id': class_id,
        'venue_id': venue_id,
        'mode': 'confirm',
        'user_id': 37181,
        'passport_venue_attended': 0,
        'passportType': 'CLASSPASS',
        'passportUsersId': 16661,
    }         

    today = datetime.combine(date.today(), time(12, 00, 05))
    subject = "ClassPass Signups Open"
    countdown(today, subject)
    print('Classes are open! Signing up for classes now!')
    print('Signing up for class: {0}'.format(class_name))
    _ = requests.post(
        URL,
        data=class_payload,
        cookies=COOKIES,
    )
    print('Request sent!')

