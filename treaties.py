from bs4 import BeautifulSoup
import urllib2
import json
import re

_list = []
_next = '/search?q={"source"%3A"treaties"}&pageSize=250'
#initializing first page and the empty list
n = 0

page_exists = True
while page_exists:
	page=urllib2.urlopen('https://www.congress.gov' + _next)
	print "Opening page https://www.congress.gov" + _next
	soup = BeautifulSoup(page.read())
	_next = soup.find('a',id = 'pagebottom_next').get('href')
	if not _next:
		page_exists = False
	li = soup.find('ol', class_ = 'results_list')
	print "found " + str(len(li)) + " treaties on the page"
	for element in li:
		n = n + 1
		print n
		treaty_link = element.find('a')
		link = treaty_link.get('href')
		opened_link = urllib2.urlopen(link)
		treaty_page = BeautifulSoup(opened_link.read())
		print "Opening treaty link: " + link
		#opened the treaty link
		plain = treaty_page.find_all('ul', class_='plain' )
		topic = plain[len(plain)-1].text.encode('ascii', 'replace')
		title = plain[0].text.encode('ascii', 'replace')
		short_title = element.find('h2').text.encode('ascii', 'replace')
		_dict = {}
		#extracted the topic and the tile
		_dict['topic'] = topic[1:len(topic)-1]
		_dict['title'] = title
		_dict['short_title'] = short_title
		print short_title
		text_link = treaty_page.find('ul', class_='tabs_links' ).find_all('a')[2].get('href')
		opened_link = urllib2.urlopen(text_link)
		text_page = BeautifulSoup(opened_link.read())
		#opened the text link
		print "Opening text link: " + text_link
		_text = text_page.find('pre')
		congress = text_page.find('h1').find('span').text
		nr = re.findall(r'\d+', congress)[0]
		_dict['congress'] = nr
		print "Congress version: " + nr
		if not not _text:
			text = _text.text.encode('ascii', 'replace')
		else:
			excuse = text_page.find('p').text.encode('ascii', 'replace')
			text = excuse
		_dict['text'] = text
		_list.append(_dict)
		print
	del soup
	del page

with open('treaties.json','w') as f:
	json.dump(_list,f)

