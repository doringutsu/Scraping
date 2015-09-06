from bs4 import BeautifulSoup
import urllib2
import os
import json

if not os.path.exists('json'):
	os.makedirs('json')

next_url = 'https://www.congress.gov/search?q={%22source%22%3A%22comreports%22%2C%22congress%22%3A%5B%22114%22%5D}&pageSize=250'

succes = False
while not succes:
	try:
		homepage = urllib2.urlopen(next_url, timeout = 1)
		succes = True
	except:
		print ('Having problems, retrying to open the url')

homesoup = BeautifulSoup(homepage.read(), 'lxml')

page = 1
cont = True
#looping through all the pages
while cont:

	ol = homesoup.find('ol')
	cells = ol.find_all('li')
  
	for i,li in enumerate(cells):
		_dict = {}

		links = li.find_all('a')
		text_url = links[0].get('href')
		title = links[0].text.encode('ascii', 'ignore')

		if len(links) > 1:
			accompanies = links[1].text
		else:
			accompanies = 'N/A'

		text_url = 'https://www.congress.gov' + text_url
		print 'Doing ' + title
		succes = False
		while not succes:
			try:
				text_page = urllib2.urlopen(text_url, timeout = 1)
				succes = True
				print ('Page opened succesfully')
				
			except:
				print ('Connection problems, retrying to open the url')

		text_soup = BeautifulSoup(text_page.read(), 'lxml')

		main = text_soup.find(id = 'report')
		text = main.find('pre').text

		

		_dict = {
		'title' : title,
		'accompanies' : accompanies,
		'text' : text
		}

		with open('json/' + str(page) + '-' + str(i) + '.json', 'w') as f:
			json.dump(_dict, f)

		print 'Done'
	
	page = page + 1
	next_url = homesoup.find('a', class_ = 'next')
	if next_url.get('href') == '#':
		break
	else:
		next_url = 'https://www.congress.gov' + next_url.get('href').encode('ascii', 'ignore')
	print 'Opening page ' + str(page) + ' ' + next_url

	succes = False
	while not succes:
		try:
			homepage = urllib2.urlopen(next_url, timeout = 1)
			succes = True
		except:
			print ('Having problems, retrying to open the url ' + next_url)

	homesoup = BeautifulSoup(homepage.read(), 'lxml')
print "Finished"