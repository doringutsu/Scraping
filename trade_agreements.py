from bs4 import BeautifulSoup
from urllib import request
from urllib.request import urlopen
import json
import re
from PyPDF2 import PdfFileReader
import os
import urllib

url = 'https://ustr.gov/trade-agreements/free-trade-agreements'
page = urlopen(url)
soup = BeautifulSoup(page.read())

div = soup.find('div', class_ = 'field-item even')
links = div.find('ul').find_all('a')

for item in links:
	country = item.text
	if not os.path.exists(country):
		os.makedirs(country)
	try:
		os.remove(country + ".json")
	except OSError:
		pass

	print (country)
	link = item.get('href')
	if 'ustr.gov' not in link:
		url = 'https://ustr.gov' + link
	else:
		url = link
	print (url)
	country_page = urlopen(url)
	country_soup = BeautifulSoup(country_page.read())
	tag = country_soup.find('a', text = 'Final Text')
	final_text = ''
	if not tag:
		final_text = 'None'
		print ('None')
	else:
		print("Opened final-text page")
		text_url =  'https://ustr.gov' + tag.get('href')
		print (text_url)
		text_page = urlopen(text_url)
		text_soup = BeautifulSoup(text_page.read())
		urls = text_soup.find('div', class_ = 'field-item even').find_all('a')
		n = 0
		for part in urls:
			n = n + 1
			part_url = 'https://ustr.gov' + part.get('href')
			part_url = part_url.replace(" ", "%20")
			print (country + " opening " + part.text)
			try:
				list_text = ""
				filename =  country + "/" + str(n) + ".pdf"
				request.urlretrieve(part_url, filename)
				pdf = PdfFileReader(open(filename, "rb"))
				for page in pdf.pages:
					list_text = list_text + page.extractText()
				with open(country + ".json", "a") as f:
					json.dump(list_text,f)
			except Exception as e: # catches any exception:
				print ("Unfortunately, the page doesn't exist")
			

			#print (part_page.read())
	print
	del country_page
	del country_soup
