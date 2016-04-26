# -*- coding: utf-8 -*-
"""

@author: SSunshine
"""

# Third Party Library Imports
import requests
import re
import sys
from datetime import date
from datetime import datetime
from datetime import time
from bs4 import BeautifulSoup

# Local Package Imports
from CP_pull import CP_get, CP_faves
from countdown import countdown

# Paste cookies from Chrome here (as unbroken string)
raw_cook = ''
 

class ClassPass(object):
    # Instantiate ClassPass object
    def __init__(self):
        # Converts the cookies obtained as a string from Chrome into dictionary
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
