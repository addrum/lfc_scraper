import json
import re
import urllib3

from bs4 import BeautifulSoup

def notify_pushbullet(pool_manager, title, message):
	pushbullet_url = 'https://api.pushbullet.com/v2/pushes'
	access_token = ''
	headers = {
		'Access-Token' : access_token,	
		'Content-Type' : 'application/json',
	}

	body = {
		'title' : title,
		'body' : message,
		'type' : 'note',
	}

	encoded_data = json.dumps(body).encode('utf-8')

	response = pool_manager.request('POST', pushbullet_url, headers=headers, body=encoded_data)
	print(response.data)
	
tickets_url = 'http://www.liverpoolfc.com/tickets/tickets-availability'

http = urllib3.PoolManager()

response = http.request('GET', tickets_url)
soup = BeautifulSoup(response.data, 'html.parser')

tag_to_search = 'span'
regex_to_search = r'.*Additional Members Sale.*'

sale_spans = soup.find_all(tag_to_search, string=re.compile(regex_to_search))

# .parent.parent.parent get's the outer "saleWrap" div which contains the buy buttons
sale_divs = [div.parent.parent.parent for div in sale_spans]

for div in sale_divs:
	btns = div.find_all('div', 'orangeBtn')

print([div.find_all('div', class_='orangeBtn') for div in sale_divs])