from bs4 import BeautifulSoup
import urllib2
import os
import json

if not os.path.exists('json'):
	os.makedirs('json')
basic_urls = [
'https://www.congress.gov/search?q={%22source%22%3A%22comreports%22%2C%22congress%22%3A%5B%22114%22%5D}&pageSize=250',
'https://www.congress.gov/search?q={%22source%22%3A%22comreports%22%2C%22congress%22%3A%5B%22113%22%5D}&pageSize=250',
'https://www.congress.gov/search?q={%22source%22%3A%22comreports%22%2C%22congress%22%3A%5B%22112%22%5D}&pageSize=250',
'https://www.congress.gov/search?q={%22source%22%3A%22comreports%22%2C%22congress%22%3A%22111%22}&pageSize=250',
'https://www.congress.gov/search?q={%22source%22%3A%22comreports%22%2C%22congress%22%3A%22110%22}&pageSize=250'
]
for i,url in enumerate(basic_urls):
	next_url = url
	year = 114 - i
	path = 'json/' + str(year)
	if not os.path.exists(path):
		os.makedirs(path)

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
					print str(page) + ' Page opened succesfully:'
				except:
					print str(page) + ' Connection problems, retrying to open the url:'

			text_soup = BeautifulSoup(text_page.read(), 'lxml')

			main = text_soup.find(id = 'report')
			text = main.find('pre').text
			pdf_url = 'https://www.congress.gov' + text_soup.find('a', text = 'PDF').get('href')
			

			_dict = {
			'title' : title,
			'accompanies' : accompanies,
			'text' : text,
			'url' : pdf_url
			}

			with open(path + '/' + str(page) + '-' + str(i) + '.json', 'w') as f:
				json.dump(_dict, f)

			print 'Done'
		
		page = page + 1
		next_url = homesoup.find('a', class_ = 'next')
		if next_url.get('href') == '#':
			cont = False
			break
		else:
			next_url = 'https://www.congress.gov' + next_url.get('href').encode('ascii', 'ignore')
		print str(year) + ' Opening new page ' + str(page) + ' ' + next_url

		succes = False
		while not succes:
			try:
				homepage = urllib2.urlopen(next_url, timeout = 1)
				succes = True
			except:
				print ('Having problems, retrying to open the url ' + next_url)

		homesoup = BeautifulSoup(homepage.read(), 'lxml')
print "Finished"