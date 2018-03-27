import json
import re
import urllib3

from bs4 import BeautifulSoup

import config

http = urllib3.PoolManager()

def notify_pushbullet(message):
	pushbullet_url = 'https://api.pushbullet.com/v2/pushes'
	headers = {
		'Access-Token' : config.PUSHBULLET_API_KEY,	
		'Content-Type' : 'application/json',
	}

	body = {
		'title' : "LFC Tickets",
		'body' : message,
		'type' : 'note',
	}

	encoded_data = json.dumps(body).encode('utf-8')

	response = http.request('POST', pushbullet_url, headers=headers, body=encoded_data)
	print(response.data)
	
tickets_url = 'http://www.liverpoolfc.com/tickets/tickets-availability'

response = http.request('GET', tickets_url)
soup = BeautifulSoup(response.data, 'html.parser')

# get the specific section for my membership level
sale_spans = soup.find_all('span', string=re.compile(r'.*Additional Members Sale.*'))

# .parent.parent.parent gets the outer "saleWrap" div which contains the buy buttons
sale_divs = [div.parent.parent.parent for div in sale_spans]

# look for the buttons with "Check Availability" as these are the ones I'll be clicking on to buy the tickets (if any are available, eek!)
check_availability_buttons = filter(bool, [div.find('a', class_='ticketBtn') for div in sale_divs])

# if there are none, alert me for debugging purposes
if check_availability_buttons is None or []:
	notify_pushbullet("No tickets available")

# https://stackoverflow.com/a/16720705/1860436 - apparently
match_info_regex = re.compile(r'\(\d+\)')
# extract the match info from the link's value and format it nicely for the PushBullet message
for button in check_availability_buttons:
	match_info = button['data-gtm-value']
	match_info = match_info_regex.sub("", match_info).strip()
	message = "{} tickets available!".format(match_info)
	notify_pushbullet(message)
