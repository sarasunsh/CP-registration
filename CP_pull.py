# -*- coding: utf-8 -*-
"""

@author: SSunshine
"""

# Third Party Library Imports
import requests

studio_URL = "https://classpass.com/a/VenueClassSchedule"
fave_URL = "https://classpass.com/favorites"


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

	studio_html = requests.post(
	    studio_URL,
	    data=payload,
	    cookies=COOKIES
	)

	return studio_html.content

def CP_faves(COOKIES):
	fave_html = requests.get(
	    fave_URL,
	    cookies=COOKIES
	)

	return fave_html.content
