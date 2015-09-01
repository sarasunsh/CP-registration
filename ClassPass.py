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
COOKIES  = {
    '__cfduid': 'd6e427245483d3e8ebe91b77c89b0edf21403099090103',
    '__qca': 'P0-755596045-1403099090930',
    'km_ai': 'AsqNnwuqhKFg0io8vbrqZEZf2M4%3D',
    'km_lv': 'x',
    'TrackJS': '5f317f37-5b03-4966-9bac-cb8a5ab83e01',
    '_hp2_id.1165694113': '2478143952259425.0739197400.2191247799',
    'km_uq': '',
    'optimizelyEndUserId': 'oeu1422464448920r0.9521982800215483',
    '__ar_v4': '4FVLTQMN6JG6JOZ7FW6XXC%3A20150225%3A204%7CLMDV4NAO45EOZLWOSAQ5LJ%3A20150225%3A253%7CKJDLOVCT6VF4TBYXFFRSW3%3A20150225%3A253%7CLX4JV2JFOJEQBCLI4P74B5%3A20150315%3A8',
    '_fbuy': '57580f55070d5a551909005205140c56000d150d550d081904015d030c0b5b03510f0903',
    'cpUtmValues': '%7B%22initial_url%22%3A%22%2F%22%7D',
    'sailthru_hid': '9fcf94234a5f45ec8b2a806ffd511e3f548099032912ffa80a8b57e07101ad1fa4e325a0524db63ce59d0c40',
    'optimizelySegments': '%7B%222331020308%22%3A%22false%22%2C%222347780571%22%3A%22gc%22%2C%222362360229%22%3A%22direct%22%7D',
    'optimizelyBuckets': '%7B%7D',
    'cpUser': 'ZWQxZjkzNWNlYjA0YTE3NjY0NTVlZjZiMTlkM2IyZWQxMzRmNzhkNDllZDIxNjhiYTFmODFiYTBkZWY5MWEyOQ%3D%3D%7CMzcxODE%3D',
    'cpVisitorId': '654614771553664e8d2dbf',
    '_gat': '1',
    '_gat_UA-25463615-3': '1',
    'classpass': 'ql4uhcd59qufast00l8et6d6p3',
    'filter_browse_venues': 'false',
    'filter_browse_neighborhoods': 'false',
    'filter_browse_activities': 'false',
    'mp_13a079f3c862893a971ff2215ef81c76_mixpanel': '%7B%22distinct_id%22%3A%20%2237181%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
    '_ga': 'GA1.2.345824304.1403099091',
    '_hp2_ses.3868021954': '*',
    '_hp2_id.3868021954': '6349802044283751.3079592812.3273501978',
    '__zlcmid': 'U1eXk35cY2NdnN'

}

def signup_for_class(class_name=None):
    payloads = {
        'Flex Studios Noho- Pilates': {
            'schedule_id': 89962187, 
            'class_id': 266544,
            'venue_id': 29254,
            'mode': 'confirm',
            'user_id': 37181,
            'passport_venue_attended': 0,
            'passportType': 'CLASSPASS',
            'passportUsersId': 16661,
        },      
        'The Path - Meditation': {
            'schedule_id': 89556149, 
            'class_id': 244420,
            'venue_id': 27950,
            'mode': 'confirm',
            'user_id': 37181,
            'passport_venue_attended': 0,
            'passportType': 'CLASSPASS',
            'passportUsersId': 16661,
        }
    }
    for class_name, class_payload in payloads.iteritems():
        print('Signing up for class: {0}'.format(class_name))
        _ = requests.post(
            URL,
            data=class_payload,
            cookies=COOKIES,
        )
        print('Request sent!')


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=(
        "Class pass automatic class signer-upper"
    ))
    today = datetime.combine(date.today(), time(12, 00, 01))
    subject = "Classpass Signups Open"
    countdown(today, subject)
    print('Classes are open! Signing up for classes now!')
    signup_for_class()



if __name__ == "__main__":
    import sys
    sys.exit(main())