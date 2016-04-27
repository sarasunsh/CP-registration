# -*- coding: utf-8 -*-
"""

@author: SSunshine
"""

# Third Party Library Imports
import csv
import datetime
import sys
from bs4 import BeautifulSoup
from transitions import Machine

# Local Package Imports
from CP_pull import CP_get, CP_faves
from CP_signup import CP_send

COOKIES = {
    '__cfduid': 'deafb60b1f8aa95ace343399570feb4211445813323',
    'optimizelyEndUserId': 'oeu1445813324715r0.6423624260351062',
    'TrackJS': 'f8c74065-2074-44ca-b938-0e45bb05d191',
    '__ar_v4': '4FVLTQMN6JG6JOZ7FW6XXC%3A20151024%3A9%7CKJDLOVCT6VF4TBYXFFRSW3%3A20151024%3A10%7CLMDV4NAO45EOZLWOSAQ5LJ%3A20151024%3A10%7CCBIW2XBJE5HBBHJDOQTAJC%3A20151024%3A1',
    'visit_count_incremented': 'true',
    'cpVisitCount': 'true',
    '__insp_wid': '324523599',
    '__insp_nv': 'true',
    '__insp_ref': 'd',
    '__insp_targlpu': 'https%3A%2F%2Fclasspass.com%2F',
    '__insp_targlpt': 'ClassPass',
    '__insp_pad': '1',
    '__insp_sid': '2845616176',
    '__insp_uid': '796953234',
    '__insp_slim': '1454557652250',
    '_hp2_id.3868021954': '3672005228684763.0206366422.3868550871',
    'sailthru_hid': '9fcf94234a5f45ec8b2a806ffd511e3f548099032912ffa80a8b57e07101ad1fa4e325a0524db63ce59d0c40',
    'cpExperimentId': '72',
    'cpGuestView': '44',
    'cpBasePlan': '36',
    'cpUtmValues': '%7B%22initial_url%22%3A%22%2F%22%7D',
    '__srret': '1',
    'optimizelySegments': '%7B%222331020308%22%3A%22false%22%2C%222347780571%22%3A%22gc%22%2C%222362360229%22%3A%22direct%22%2C%223537322437%22%3A%22none%22%7D',
    'optimizelyBuckets': '%7B%223544160422%22%3A%220%22%7D',
    '_gat': '1',
    'bounceClientVisit1678v': '{"lp":"https%3A%2F%2Fclasspass.com%2Flogin%2Ffavorites","r":""}',
    'cpUser': 'Njk1MDMzODU0OGYzZGFjNmFmNDU5MGYzYTBkZTIyY2EwM2MwOTZmODFlMzY3ODQwNGQ1YTQzN2VmYTNkNmUxMA%3D%3D%7CMzcxODE%3D',
    'cpUserType': 'subscribed',
    'cpVisitorId': '518335952562d5be42735e',
    'classpass': 'lab0u0rihln8005783c3ob9kt4',
    '_ga': 'GA1.2.1800631415.1445813325',
    'mp_mixpanel__c': '1',
    'mp_13a079f3c862893a971ff2215ef81c76_mixpanel': '%7B%22distinct_id%22%3A%20%2237181%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22msa_id%22%3A%20null%2C%22msa_name%22%3A%20null%2C%22user_type%22%3A%20%22subscribed%22%2C%22count_lifetime_visits%22%3A%202%2C%22first_visit_date%22%3A%20%222016-01-03%22%2C%22guest_view%22%3A%20%22false%22%2C%22user_id%22%3A%20%2237181%22%2C%22session_start_count%22%3A%209%2C%22app_platform%22%3A%20%22web%22%2C%22device_type%22%3A%20%22desktop%22%7D',
    '_fbuy': '560a0c51025d0c0419005a5503140c015508150c500d0119500a5c55505a0c03550c0d52',
    '_fbuy_buckets': '%7B%22bsy-f4y%22%3A%5B22716%2C1460426609793%5D%7D',
    '__zlcmid': 'XNf3Qzrg2WGkYB',
    'bounceClientVisit1678': '{"sid":3,"fvt":1456074086,"vid":1460426441497287,"ao":4,"as":0,"vpv":3,"d":"d","lp":"https%3A%2F%2Fclasspass.com%2Flogin%2Ffavorites","r":"","cvt":1460426441,"gcr":49,"m":0,"did":"1876252171476399688","lvt":1460426616,"v":{"user_email":false,"zip_code":false,"ever_logged_in":true,"map_studios_count":0,"map_city_name":0},"campaigns":{"254716":{"lvt":1460209491,"lavid":1},"254724":{"lvt":1457918720,"lavid":1,"la":1457918720,"fsa":1457648332,"as":1,"ao":4}}}'

}

# Pull list of favorite studios from ClassPass
fave_html = CP_faves(COOKIES)
studio_deets = BeautifulSoup(fave_html, "lxml")

favorites = studio_deets.find_all("li", class_="grid__item md-1/2 lg-1/3")

studio_dict = {}

for fave in favorites:
    blurb = fave.find("h2")
    url = blurb.a["href"].split("/")
    venue_id = fave.find("a").get("data-venue-id")
    studio_dict[url[-1]] = venue_id


##TO DO: figure out better way to handle this? also confirm that a day < 10 needs leading zero added
# today_date = time.strftime("20%y-%m-%d")
now = datetime.datetime.now()
if now.month < 10:
    month = "0"+str(now.month)
else:
    month = str(now.month)

if now.day < 10:
    day = "0"+str(now.day + 6)
else:
    day = str(now.day + 6)

next_week = str(now.year)+"-"+month+"-"+day

# Implementation of state machine based on example at link below:
#https://groups.google.com/forum/#!topic/comp.lang.python/z2LWpspqDWA

##### 
# Functions for each state go here. They end by setting CURRENT_STATE to some value 
##### 

def display_faves(): 
    global CURRENT_STATE

    # Display studio options and allow user to select one
    for i, name in enumerate(studio_dict.keys()):
        print i, name

    response = raw_input("Please enter the studio number you're interested in: ")

    venue_id = studio_dict.items()[int(response)][1]
    venue_name = studio_dict.items()[int(response)][0]

    CURRENT_STATE = "studio"
    return venue_id, venue_name

def pull_classes(): 
    global CURRENT_STATE, classes

    # Feed this venue_id into CP_pull.py to retrieve html 
    studio_html = CP_get(venue_id, next_week, COOKIES)

    # Use BeautifulSoup to pull link, title, and time information for classes 
    soup = BeautifulSoup(studio_html, "lxml")
    classes = soup.find_all("li", class_="venue-class clearfix inactive")

    class_ids = []
    class_names =[]
    sched_ids = []
    start_times = []
    end_times = []
    class_dates = []

    for item in classes:
       class_ids.append(item.get('data-class-id'))
       class_names.append(item.get('data-class-name'))
       sched_ids.append(item.get('data-schedule-id'))
       start_times.append(item.get('data-start-time'))
       end_times.append(item.get('data-end-time'))
       class_dates.append(item.get('data-class-date'))

    # Display class options
    print "\n %s offers the following classes on %s:" % (venue_name, class_dates[0])
    for j in range(len(class_ids)):
        print j, class_names[j], str(start_times[j])+" - "+str(end_times[j])

    # Prompt for user input
    response = raw_input("Enter 1 if you would like to add a class to cart, 2 if you would like to look at the cart, and 3 if you would like to return to favorites: ")

    if response == 1:
        int_r = int(response)

        print "\n You have added: ", venue_name, class_names[int_r], str(start_times[int_r])+"-"+str(end_times[int_r])

        class_deets = [sched_ids[int_r], venue_id, class_ids[int_r], class_names[int_r], venue_name, str(start_times[int_r])+"-"+str(end_times[int_r])]
        classes.append(class_deets)

        CURRENT_STATE = "cart"

    elif response == 2:
        CURRENT_STATE = "cart"

    elif response == 3:
        CURRENT_STATE = "favorites"

def see_cart():
    global CURRENT_STATE, classes

    for i, cl in enumerate(classes):
        print i, cl[-3:]

    response = raw_input("Press 1 if you are ready to sign up, 2 if would like to remove a class, and 3 to return to favorites: ")

    if response == 1:
        CURRENT_STATE = "check out"
    elif response == 2:
        response2 = raw_input("Please enter the number of the class you would like remove: ")
        ## INSERT CODE HERE
    elif response == 3:
        CURRENT_STATE = "favorites"

def sign_up():
    global CURRENT_STATE

    print classes
    ## ADD CODE HERE

    CURRENT_STATE = "Done"

CURRENT_STATE = "favorites"
DFA_STATE_MACHINE = {"favorites" : display_faves, "studio" : pull_classes, 
"cart" : see_cart, "check out": sign_up} 
classes = []


# Now run the state machine 
while ( CURRENT_STATE != "Done"): 
     # Execute the function for the current state 
     DFA_STATE_MACHINE[CURRENT_STATE]() 
