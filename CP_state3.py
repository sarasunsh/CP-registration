# -*- coding: utf-8 -*-
"""

@author: SSunshine
"""

# Third Party Library Imports
import requests
import re
import sys
from datetime import date, datetime, time, timedelta
from bs4 import BeautifulSoup

# Local Package Imports
from CP_pull import CP_get, CP_faves
from countdown import countdown

# Paste cookies from Chrome here (as unbroken string)
raw_cook = '__cfduid=d6e427245483d3e8ebe91b77c89b0edf21403099090103; km_ai=AsqNnwuqhKFg0io8vbrqZEZf2M4%3D; km_lv=x; TrackJS=5f317f37-5b03-4966-9bac-cb8a5ab83e01; _hp2_id.1165694113=2478143952259425.0739197400.2191247799; km_uq=; optimizelyEndUserId=oeu1422464448920r0.9521982800215483; __ar_v4=4FVLTQMN6JG6JOZ7FW6XXC%3A20150225%3A204%7CLMDV4NAO45EOZLWOSAQ5LJ%3A20150225%3A253%7CKJDLOVCT6VF4TBYXFFRSW3%3A20150225%3A253%7CLX4JV2JFOJEQBCLI4P74B5%3A20150315%3A8; sailthru_hid=9fcf94234a5f45ec8b2a806ffd511e3f548099032912ffa80a8b57e07101ad1fa4e325a0524db63ce59d0c40; _hp2_id.3868021954=6349802044283751.3780338889.1752130478; __insp_slim=1458137781396; __insp_wid=324523599; __insp_nv=true; __insp_ref=d; __insp_targlpu=https%3A%2F%2Fclasspass.com%2F; __insp_targlpt=ClassPass; __insp_norec_sess=true; cpExperimentId=56; cpUtmValues=%7B%22initial_url%22%3A%22%2F%22%7D; cpGuestView=6; cpBasePlan=15; cpCohort=false_base_2; cpVisitCount=true; CP.SID=eyJhdXRoVG9rZW4iOiI0NjcwNmRkNDcxMmJkZTA4NjVhNTM4NTI1YTAzY2UyMDA2YzViZGU1In0=; CP.SID.sig=m3IDx9vQ90a4qLpE6oIm0_GQ-J0; cpUser=NDE3OGNhYjM0ZDNjYzY4ZWYxMTBmNDAyN2Q1YzQ5MDU0ZGM5MWM0NDI1NTdlZGFmNjBlOGRmZmRiMmE1ZTFlMQ%3D%3D%7CMzcxODE%3D; cpVisitorId=654614771553664e8d2dbf; classpass=ce0c4caea8c7d4360d75091660be5b21; optimizelySegments=%7B%222331020308%22%3A%22false%22%2C%222347780571%22%3A%22gc%22%2C%222362360229%22%3A%22direct%22%2C%223537322437%22%3A%22none%22%7D; optimizelyBuckets=%7B%223544160422%22%3A%220%22%7D; bounceClientVisit1678v={"lp":"https%3A%2F%2Fclasspass.com%2Fhome","r":""}; cpUserType=subscribed; _ga=GA1.2.345824304.1403099091; mp_13a079f3c862893a971ff2215ef81c76_mixpanel=%7B%22distinct_id%22%3A%20%2237181%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22utm_source%22%3A%20%22classpass%22%2C%22utm_medium%22%3A%20%22email%22%2C%22utm_campaign%22%3A%20%22Email%22%2C%22utm_content%22%3A%20%228212%22%2C%22msa_id%22%3A%201%2C%22msa_name%22%3A%20%22New%20York%20Metro%22%2C%22user_type%22%3A%20%22prospect%22%2C%22count_lifetime_visits%22%3A%209%2C%22first_visit_date%22%3A%20%222015-12-23%22%2C%22guest_view%22%3A%20%22false_base_2%22%2C%22user_id%22%3A%20%2237181%22%2C%22session_start_count%22%3A%2013%2C%22app_platform%22%3A%20%22web%22%2C%22device_type%22%3A%20%22desktop%22%2C%22%24search_engine%22%3A%20%22google%22%7D; __srret=1; _fbuy=065a0850555f0e51195f080505140c56070b150d030f0d19050c5b0c055d5e0c000d0b01; _fbuy_buckets=%7B%22bsy-f4y%22%3A%5B22716%2C1461768341886%5D%7D; bounceClientVisit1678={"sid":16,"fvt":1455722728,"vid":1461767954432817,"ao":2,"as":0,"vpv":15,"d":"d","lp":"https%3A%2F%2Fclasspass.com%2Fhome","r":"","cvt":1461767954,"gcr":63,"m":0,"did":"6300588047857816873","lvt":1461768373,"v":{"user_email":false,"zip_code":false,"ever_logged_in":true,"map_studios_count":0,"map_city_name":0,"user_type":"subscribed","data_msa_city_name":false,"data_msa_body_class":"profiles body--detail body--sticky-footer passport"},"campaigns":{"254724":{"lvt":1458052717,"lavid":1,"la":1458052717,"fsa":1457971052,"as":1,"ao":2}},"hc_home":1}; __zlcmid=U1eXk35cY2NdnN; mp_mixpanel__c=28'


class ClassPass(object):
    # Instantiate ClassPass object
    def __init__(self):
        # Converts the cookies obtained as a string from Chrome into dictionary
        raw_cook.replace('=;',';')
        cook_list = re.split('=|;', raw_cook)
        i = 0
        COOKIES = {}
        while i < (len(cook_list) - 1):
            if i%2==0:
                COOKIES[cook_list[i]] = cook_list[i+1]
            i +=1

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

        # Get next week's date
        next_week = datetime.now() + timedelta(days=6)
        next_week_s = next_week.strftime("20%y-%m-%d")

        # Initialize
        self.studio_dict = studio_dict
        self.next_week_s = next_week_s
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
        studio_html = CP_get(self.venue_id, self.next_week_s, self.cookies)

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

        # print self.next_week_s
        # print studio_classes
        # Display class schedule options
        # BUG: If there are no classes being offered next week, class_dates[0] will throw an indexing error.
        print "\n %s offers the following classes on %s:" % (self.venue_name, class_dates[0])
        for j in range(len(class_ids)):
            print j, class_names[j], str(start_times[j])+" - "+str(end_times[j])
 
        # Prompt for user input
        class_prompt = input("Enter 1 if you would like to add a class to cart, 2 if you would like to look at the cart, and 3 if you would like to return to favorites: ")
        if class_prompt == 1:
            
            class_num = input("Please enter the number of the class you'd like to add to the cart: ")
            
            # Set class details for selected class
            sched_id = sched_ids[class_num]
            class_id = class_ids[class_num]
            class_name = class_names[class_num]
            class_time = str(start_times[class_num])+"-"+str(end_times[class_num])
            class_deets = [sched_id, self.venue_id, class_id, class_name, self.venue_name, class_time]
            
            # Add selected class to cart
            self.classes_in_cart.append(class_deets)
            self.display_cart()

        elif class_prompt == 2:
            self.display_cart()

        elif class_prompt == 3:
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
