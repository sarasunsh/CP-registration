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

}

def signup_for_class(class_name=None):
    payloads = {
        
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
