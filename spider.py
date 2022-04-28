import re, requests, time, argparse, sys, traceback
from fake_useragent import UserAgent
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from selenium import webdriver
from bs4 import BeautifulSoup

class Spider:
	
	def __init__(self,url):
		self.storeLinks = []
		self.ua = UserAgent()
		self.url = url
		self.session = requests.Session()
		
	def parseLinks(self,get): #using regex to parse href links not bs yet, returns a list 
		if isinstance(get,bytes):
			try:
				get = get.decode()
			except:
				get = str(get)
		return re.findall('(?:href=")(.*?)"',get) #returns list of matches 

	def crawlerSel(self,url):
		parsedLinks = self.parseLinks(self.selGet(url))
		for link in parsedLinks:
			if not link.endswith('feed/'):
				if 'http' not in link or 'https' not in link:
					link = urljoin(url,link)	
				if '#' in link:
					link = link.split('#')[0]
				if self.url in link and link not in self.storeLinks:
					self.storeLinks.append(link)
					#print(link)
					try:
						self.crawlerSel(link)
					except:
						#print(f'\nCould not extract links from {link}\n')
						#print(f'link is stored: {link in self.storeLinks}')
						pass
			else:
				if link not in self.storeLinks:
					self.storeLinks.append(link)
					#print(link)
					#print(f'link is stored: {link in self.storeLinks}')
					
	def crawlerReq(self,url):
		parsedLinks = self.parseLinks(self.reqGet(url))
		for link in parsedLinks:
			if 'http' not in link and 'https' not in link:
				link = urljoin(url,link)
			if '#' in link:
				link = link.split('#')[0]
			if url in link and link not in self.storeLinks:
				self.storeLinks.append(link)
				#print(link)
				try:
					self.crawlerReq(link)
				except:
					#print(f'Could not extract links from {link}')
					#print(f'link is stored: {link in self.storeLinks}')
					pass
			
	def crawlerBase(self,url): #Non-recursive, just collects href links, has options for sel or req
		while True:
			checkType = input('Enter \'sel\' for selenium or \'req\' for requests\n:')
			if checkType in ['sel', 'req']:
				break
		if checkType == 'sel':
			parsedLinks = self.parseLinks(self.selGet(url))
		elif checkType == 'req':
			parsedLinks = self.parseLinks(self.reqGet(url))
		links = []
		for link in self.parseLinks(self.selGet(url)):
			if 'http' or 'https' not in link:
				link = urljoin(url,link)
			if '#' in link:
				link = link.split('#')[0]
			if url in link and link not in self.storeLinks:
				#print(link)
				self.storeLinks.append(link)
		#return self.storeLinks

	def reqGet(self,url):
		try:
			response = self.session.get(url,headers = {'User-Agent': self.ua.random})
			if response.status_code == 200:
				return response.content
		except Exception:
			print(traceback.format_exc())
			return None

	def gethtmlLib(self,url=None):
		if url == None:
			url = self.url
		page = Request(url, headers = {'User-Agent':self.ua.random})
		print(page)
		webpage = urlopen(page).read()
		print(webpage)

	def selGet(self, url=None):
		if url == None:
			url = self.url
		fireFoxOptions = webdriver.FirefoxOptions()
		fireFoxOptions.headless = True
		browser = webdriver.Firefox(options = fireFoxOptions)
		browser.get(url)
		return (browser.page_source)# when requests or self.urllib does not work, can run selenium headless to get page source
	
	def run(self):
		if not self.url.endswith('/'):
			self.url = self.url + '/'
		while True:
			validateURL = input(f'Confirm URL: {self.url}\nURL Correct? y/n\n:')
			validateURL = validateURL.lower()
			if validateURL == 'y':
				break
			elif validateURL == 'n':
				print('URL error, Qutting...')
				sys.exit()
		while True:
			runType = input('Enter \'sel\' to use selenium | \'req\' to use requests | \'get\' to parse links for one url\n:')
			if runType in  ['sel', 'req', 'get']:
				break
		if runType == 'sel':
			self.crawlerSel(self.url)
		elif runType == 'req':
			self.crawlerReq(self.url)
		elif runType == 'get':
			self.crawlerBase(self.url)

########################################################RUN###################################################################
#try:
	#spider = Spider('http://192.168.86.115')
	#linklist = spider.parseLinks(spider.selGet())
	#print(linklist)
	#spider.run()
	#print(spider.storeLinks)
#except:
	#print(traceback.format_exc())


