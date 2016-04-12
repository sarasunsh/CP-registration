# -*- coding: utf-8 -*-
"""

@author: SSunshine
"""

# Third Party Library Imports
import csv
from bs4 import BeautifulSoup
import datetime
import sys

# Local Package Imports
from CP_pull import CP_get, CP_faves
from CP_signup import CP_send

COOKIES = {

}

# Function that checks if the input is a valid selection
## TO DO: better way to do this?
def error_check(response):
    try:
        int(response)
    except ValueError:
        print "That is not a number."
        return True

    if int(response) < 0 or int(response) >= len(studio_dict):
        print "That number does not correspond to a studio."
        return True
    else:
        return False

# Pull list of favorite studios from ClassPass
fave_html = CP_faves(COOKIES)
studio_deets = BeautifulSoup(fave_html, "lxml")

# Check if cookies are valid
## TO DO: this is a little hacky -- better way?
if len(studio_deets.final_all("header", class_="header js-log-state")) == 0:
    print "Log-in failed. You may need to update your cookies."
    sys.exit()


favorites = studio_deets.find_all("li", class_="grid__item md-1/2 lg-1/3")

studio_dict = {}

for fave in favorites:
    blurb = fave.find("h2")
    url = blurb.a["href"].split("/")
    venue_id = fave.find("a").get("data-venue-id")
    studio_dict[url[-1]] = venue_id
    
# Display studio options
for i, name in enumerate(studio_dict.keys()):
	print i, name

# Get user input on studio choice 
response = raw_input("Please enter the studio number: ")

# Check if number entered is not valid key
tries = 0
while error_check(response) and tries <3:
    tries += 1
    response = raw_input("That was not a valid studio number. Try again: ")

venue_id = studio_dict.items()[int(response)][1]
venue_name = studio_dict.items()[int(response)][0]

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


# links = [link.a["href"] for link in soup.find_all("li", class_="col01")]
# titles = [link.text.encode('utf-8').strip() for link in soup.find_all("li", class_="col01")]
# times = [item.text.encode('utf-8') for item in soup.find_all("li", class_="col02")]

# Display class options
print "\n %s offers the following classes on %s:" % (venue_name, class_dates[0])
for j in range(len(class_ids)):
    print j, class_names[j], str(start_times[j])+" - "+str(end_times[j])

# Get user input on class choice 
response2 = raw_input("Please enter the number of the class you'd like to take: ")
if error_check(response2):
    response2 = raw_input("That was not a valid class number. Please try again: ")
int_r = int(response2)

print "\n You selected: ", venue_name, class_names[int_r], str(start_times[int_r])+"-"+str(end_times[int_r])

#Use the above information to call sign-up function 
CP_send(sched_ids[int_r], venue_id, class_ids[int_r], class_names[int_r], COOKIES)


