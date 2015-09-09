from bs4 import BeautifulSoup
import urllib2
import os
import json
import urllib
from PyPDF2 import PdfFileReader

url = 'http://appropriations.house.gov/subcommittees/'
homepage = urllib2.urlopen(url)
homesoup = BeautifulSoup(homepage.read(), 'lxml')

directory = 'draft-reports'
if not os.path.exists(directory):
	os.makedirs(directory)

urls = homesoup.find('ul', id = 'menu').find_all('a')

for url in urls:
	if 'Related Documents' in url.text:
		doc_url = 'http://appropriations.house.gov'  + url.get('href')
		doc_page = urllib2.urlopen(doc_url)
		doc_soup = BeautifulSoup(doc_page)

		file_urls = doc_soup.find('ul', class_ = 'UnorderedFileList').find_all('a')
		for url in file_urls:
			if ('FY 2016' in url.text or 'FY 2015' in url.text) and 'Draft Committee' in url.text:
				print 'Downloading ' + url.text
				filename =  url.text + '.json'
				pdf_url = 'http://appropriations.house.gov' + url.get('href')
				urllib.urlretrieve(pdf_url, 'temp.pdf')
				pdf = PdfFileReader(open('temp.pdf', "rb"))

				report_text = ''
				for page in pdf.pages:
					report_text = report_text + page.extractText()

				with open(directory + '/' + filename, 'w')as f:
					json.dump(report_text, f)