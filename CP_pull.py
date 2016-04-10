# -*- coding: utf-8 -*-
"""

@author: SSunshine
"""

# Third Party Library Imports
import requests
from bs4 import BeautifulSoup

URL = "https://classpass.com/a/VenueClassSchedule"

def CP_get(venue_id, next_week, COOKIES):
	payload = {
		'venue_id':venue_id, 
		'passport':1,
		'passport_sell':0,
		'passport_reservable':1,
		'passport_status':'default',
		'passportType':'CLASSPASS',
		'week_date': next_week,
		'direction':'next',
		'less_days':7,
	}

	start_url = requests.post(
	    URL,
	    data=payload,
	    cookies=COOKIES
	)

	return start_url.content