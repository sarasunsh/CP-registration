#!/usr/bin/env python
"""
"""

# Third Party Library Imports
import requests
from datetime import date
from datetime import datetime
from datetime import time
import csv

# Local Package Imports
from countdown import countdown

URL = "https://classpass.com/a/PassportReserveDialog"

COOKIES  = {
  
}

# Read classlist from CSV
def import_classes_from_csv():
    reader = csv.reader(open('classlist.csv'))
    class_dict = {}
    for row in reader:
        key = row[0]
        # Skip duplicates
        if key in class_dict:
            pass
        class_dict[key] = row[1:]
    
    print "CSV imported"    
    return class_dict

# Create payloads to be sent to the site
def generate_payloads(classes, class_dict):
    payloads = {}
    for workout in classes:
        
        # Split the workout url into 2 pieces: class name, schedule
        workout = workout.split('/')
        
        # Check that the url was able to be properly split
        if len(workout) != 2:
            return 'The following input does not have correct format: '+str(workout)
        
        url_name = workout[0]
        schedule_id = int(workout[1])
        class_name = class_dict[url_name][0]
        class_id = int(class_dict[url_name][1])
        venue_id = int(class_dict[url_name][2])
        
        payloads[class_name] =  {
            'schedule_id': schedule_id, 
            'class_id': class_id,
            'venue_id': venue_id,
            'mode': 'confirm',
            'user_id': 37181,
            'passport_venue_attended': 0,
            'passportType': 'CLASSPASS',
            'passportUsersId': 16661,
        }
        
    print "Payloads generated"
    return payloads

def signup_for_class(payloads):
                      
    for class_name, class_payload in payloads.iteritems():
        print('Signing up for class: {0}'.format(class_name))
        _ = requests.post(
            URL,
            data=class_payload,
            cookies=COOKIES,
        )
        print('Request sent!')

def main(classes):   
    class_dict = import_classes_from_csv()    
    payloads = generate_payloads(classes, class_dict)
    today = datetime.combine(date.today(), time(12, 00, 30))
    subject = "Classpass Signups Open"
    countdown(today, subject)
    print('Classes are open! Signing up for classes now!')
    signup_for_class(payloads)

#
#
#if __name__ == "__main__":
#    import sys
#    sys.exit(main(classes))
