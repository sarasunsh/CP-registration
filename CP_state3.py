# -*- coding: utf-8 -*-
"""

@author: SSunshine
"""

# Third Party Library Imports
import requests
import sys
from datetime import date
from datetime import datetime
from datetime import time
from bs4 import BeautifulSoup

# Local Package Imports
from CP_pull import CP_get, CP_faves
from countdown import countdown


## Change cookie_parser so it no longer prints but instead stores reformatted cookies
COOKIES = {
    '__cfduid': 'deafb60b1f8aa95ace343399570feb4211445813323',
    'optimizelyEndUserId': 'oeu1445813324715r0.6423624260351062',
    'TrackJS': 'f8c74065-2074-44ca-b938-0e45bb05d191',
    '__ar_v4': '4FVLTQMN6JG6JOZ7FW6XXC%3A20151024%3A9%7CKJDLOVCT6VF4TBYXFFRSW3%3A20151024%3A10%7CLMDV4NAO45EOZLWOSAQ5LJ%3A20151024%3A10%7CCBIW2XBJE5HBBHJDOQTAJC%3A20151024%3A1',
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
    'cpUtmValues': '%7B%22initial_url%22%3A%22%2F%22%7D',
    'cpGuestView': '44',
    'cpBasePlan': '36',
    'optimizelySegments': '%7B%222331020308%22%3A%22false%22%2C%222347780571%22%3A%22gc%22%2C%222362360229%22%3A%22direct%22%2C%223537322437%22%3A%22none%22%7D',
    'optimizelyBuckets': '%7B%223544160422%22%3A%220%22%7D',
    '_gat': '1',
    'bounceClientVisit1678v': '{"lp":"https%3A%2F%2Fclasspass.com%2Flogin%2Ffavorites","r":""}',
    'cpUser': 'NDIwYmY3MzBiMjBkZmJmY2ZjNGFlNGJlNjhjNDExNDUzNDUzMzc4YzliOTJiM2U2ODEzZTM3ZjMwOGY4ZmNkOQ%3D%3D%7CMzcxODE%3D',
    'cpVisitorId': '518335952562d5be42735e',
    'classpass': '4b916dab6d1cc5277a48d10443e80dfb',
    '_ga': 'GA1.2.1800631415.1445813325',
    'mp_13a079f3c862893a971ff2215ef81c76_mixpanel': '%7B%22distinct_id%22%3A%20%2237181%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22msa_id%22%3A%20%221%22%2C%22msa_name%22%3A%20%22New%20York%20Metro%22%2C%22user_type%22%3A%20%22prospect%22%2C%22count_lifetime_visits%22%3A%202%2C%22first_visit_date%22%3A%20%222016-01-03%22%2C%22guest_view%22%3A%20%22false_base_2%22%2C%22user_id%22%3A%20%2237181%22%2C%22session_start_count%22%3A%2015%2C%22app_platform%22%3A%20%22web%22%2C%22device_type%22%3A%20%22desktop%22%7D',
    '__srret': '1',
    '_fbuy': '560a0c51025d0c0419005a5503140c015508150c500d0119500a5c55505a0c03550c0d52',
    '_fbuy_buckets': '%7B%22bsy-f4y%22%3A%5B22716%2C1461547639143%5D%7D',
    '__zlcmid': 'XNf3Qzrg2WGkYB',
    'bounceClientVisit1678': '{"sid":2,"fvt":1456074086,"vid":1461547634716852,"ao":4,"as":0,"vpv":2,"d":"d","lp":"https%3A%2F%2Fclasspass.com%2Flogin%2Ffavorites","r":"","cvt":1461547634,"gcr":49,"m":0,"did":"1876252171476399688","lvt":1461547640,"v":{"user_email":false,"zip_code":false,"ever_logged_in":true,"map_studios_count":0,"map_city_name":0,"user_type":"subscribed"},"campaigns":{"254716":{"lvt":1460209491,"lavid":1},"254724":{"lvt":1457918720,"lavid":1,"la":1457918720,"fsa":1457648332,"as":1,"ao":4}},"hc_home":1}',
    'cpUserType': 'subscribed',
    'mp_mixpanel__c': '7'
}

class ClassPass(object):

    # Initantiate ClassPass object
    def __init__(self):
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
        now = datetime.now()
        if now.month < 10:
            month = "0"+str(now.month)
        else:
            month = str(now.month)
        if now.day < 10:
            day = "0"+str(now.day + 6)
        else:
            day = str(now.day + 6)
        next_week = str(now.year)+"-"+month+"-"+day

        self.studio_dict = studio_dict
        self.next_week = next_week
        self.cookies = COOKIES
        self.classes_in_cart = []
        self.display_studios()

    # Display studio options from user's favorites list
    def display_studios(self):
        for i, name in enumerate(self.studio_dict.keys()):
            print i, name
        self.select_studio()

    # Prompt user to select a studio to see its schedule
    def select_studio(self):
        self.studio_num = input("Please enter the studio number you're interested in: ")

        self.venue_id = self.studio_dict.items()[self.studio_num][1]
        self.venue_name = self.studio_dict.items()[self.studio_num][0]

        self.display_classes()

    # Display next week's classes for the selected studio
    def display_classes(self):

        # Feed venue_id into function to retrieve html 
        studio_html = CP_get(self.venue_id, self.next_week, self.cookies)

        # Use BeautifulSoup to pull link, title, and time information for classes 
        soup = BeautifulSoup(studio_html, "lxml")
        studio_classes = soup.find_all("li", class_="venue-class clearfix inactive")

        class_ids = []
        class_names =[]
        sched_ids = []
        start_times = []
        end_times = []
        class_dates = []

        for item in studio_classes:
           class_ids.append(item.get('data-class-id'))
           class_names.append(item.get('data-class-name'))
           sched_ids.append(item.get('data-schedule-id'))
           start_times.append(item.get('data-start-time'))
           end_times.append(item.get('data-end-time'))
           class_dates.append(item.get('data-class-date'))

        # BUG: If there are no classes being offered next week, class_dates[0] will throw an indexing error.
        # Display class schedule options
        print "\n %s offers the following classes on %s:" % (self.venue_name, class_dates[0])
        for j in range(len(class_ids)):
            print j, class_names[j], str(start_times[j])+" - "+str(end_times[j])
 
        # Prompt for user input
        self.class_prompt = input("Enter 1 if you would like to add a class to cart, 2 if you would like to look at the cart, and 3 if you would like to return to favorites: ")
        if self.class_prompt == 1:
            
            self.class_num = input("Please enter the number of the class you'd like to add to the cart: ")
            
            # Set class details for selected class
            self.sched_id = sched_ids[self.class_num]
            self.class_id = class_ids[self.class_num]
            self.class_name = class_names[self.class_num]
            self.class_time = str(start_times[self.class_num])+"-"+str(end_times[self.class_num])
            class_deets = [self.sched_id, self.venue_id, self.class_id, self.class_name, self.venue_name, self.class_time]
            
            # Add selected class to cart
            self.classes_in_cart.append(class_deets)
            self.display_cart()

        elif self.class_prompt == 2:
            self.display_cart()

        elif self.class_prompt == 3:
            self.display_studios()

    # Print the details for classes currently in cart and allow the user to modify the cart content
    def display_cart(self):
        print "Your cart contains the following classes: "
        for i, cl in enumerate(self.classes_in_cart):
            print i, cl[-3:]

        self.cart_prompt = input("Press 1 if you are ready to sign up, 2 if would like to remove a class, and 3 to return to favorites: ")

        if self.cart_prompt == 1:
            self.sign_up()
        elif self.cart_prompt == 2:
            self.removed_class_i = input("Please enter the number of the class you would like remove: ")
            self.classes_in_cart.pop(self.removed_class_i)
            self.display_cart()
        elif self.cart_prompt == 3:
            self.display_studios()

    # Execute sign-up process for classes in cart
    def sign_up(self):
        payloads = {}
        URL = "https://classpass.com/a/PassportReserveDialog"
        for workout in self.classes_in_cart:       
            payloads[workout[3]] =  {
                'schedule_id': workout[0], 
                'class_id': workout[2],
                'venue_id': workout[1],
                'mode': 'confirm',
                'user_id': 37181,
                'passport_venue_attended': 0,
                'passportType': 'CLASSPASS',
                'passportUsersId': 16661,
            }

        today = datetime.combine(date.today(), time(12, 00, 30))
        subject = "Classpass Signups Open"
        countdown(today, "ClassPass Signups Open")
        print('Classes are open! Signing up for classes now!')

        for class_name, class_payload in payloads.iteritems():
            print('Signing up for class: {0}'.format(class_name))
            _ = requests.post(
                URL,
                data=class_payload,
                cookies=COOKIES,
            )
        sys.exit()

ClassPass()
