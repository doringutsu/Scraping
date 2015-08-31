from bs4 import BeautifulSoup
import urllib2
import os
import json

directory = 'bills'
if not os.path.exists(directory):
    os.makedirs(directory)
url = 'http://www.senate.gov/reference/Legislation/Appropriations/2016.htm'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read(), 'lxml')
table = soup.find('table', class_ = 'contenttext')
rows = table.find_all('tr')

for row in rows:
	try:
		cell = row.find_all('td')[2]
	except Exception:
		continue
	links = cell.find_all('a')

	for link in links:
		name = link.text
		bill_url =  link.get('href')
		print "Opening " + bill_url
		bill_page = urllib2.urlopen(bill_url)
		bill_soup = BeautifulSoup(bill_page.read(),'lxml')
		tab = bill_soup.find('ul', class_ = 'tabs_links')
		cell = tab.find_all('li')[1]
		text_url = cell.find('a').get('href') + '?format=txt'
		print "  Opening text page " + text_url
		text_page = urllib2.urlopen(text_url)
		text_soup = BeautifulSoup(text_page.read(),'lxml')
		_text = text_soup.find('pre').text
		print "Writing file " + directory + '/' + name + ".json"
		with open(directory + '/' + name + ".json", 'w') as f:
			json.dump(_text,f)		
		del bill_page
		del bill_soup
		del text_page
		del text_soup
