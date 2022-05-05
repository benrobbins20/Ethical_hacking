import re, requests, time, argparse, sys, traceback
from fake_useragent import UserAgent
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from selenium import webdriver
from bs4 import BeautifulSoup

class fc:
    rw = '\033[31;107m'
    r = '\033[38;5;196m'
    pv = '\033[38;5;206;48;5;57m'
    end = '\033[0m'
    p = '\033[38;5;206m'
    y = '\033[0;33;40m'
    pu = '\033[0;35m'
    wg = '\033[37;42m'
    cy = '\033[36m'
    g = '\033[38;5;154m'
    b = '\033[38;5;45m'

class Spider:
	def __init__(self,url,ignore=None): #ignore is an array of links to ignore, (logout.php)
		self.storeLinks = []
		self.ua = UserAgent()
		self.url = url
		self.session = requests.Session()
		self.ignore = ignore
		print(f'{fc.pu}#{fc.end}'*100)
		print(f'{fc.cy}Spider session created:{fc.end} {fc.wg}{self.session}{fc.end}')
		
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
			if url in link and link not in self.storeLinks and link not in self.ignore:
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
			else:
				return None
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
		# while True:
		# 	validateURL = input(f'Confirm URL: {self.url}\nURL Correct? y/n\n:')
		# 	validateURL = validateURL.lower()
		# 	if validateURL == 'y':
		# 		break
		# 	elif validateURL == 'n':
		# 		print('URL error, Qutting...')
		# 		sys.exit()
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

	def getForms(self,url):
		response = self.session.get(url,headers = {'User=Agent': self.ua.random})
		if b'</form>' in response.content: # simple check to see if there is a form tag
			soup = BeautifulSoup(response.content,'html.parser')
			forms = soup.findAll('form') # returns list of forms found by bs 
			return forms
		

	def postForm(self,forms,value,url): # can pass a list in for forms but should only be 1 item
		for form in forms:
			action = form.get('action')
			fullurl = (urljoin(url, action))
			method = form.get('method')
			print(
			f'\n{fc.p}Link: {fullurl}{fc.end}\n'
			f'{fc.p}Action: {action}{fc.end}'
			)
			inputList = form.findAll('input')
			postData = {}
			for i in inputList:
				inputName = i.get('name')
				inputType = i.get('type')
				inputValue = i.get('value')
				if inputType == 'text':
					inputValue = value
				postData[inputName] = inputValue
				if method == 'post':
					return self.session.post(fullurl,data=postData)
				return self.session.get(fullurl,params=postData)

########################################################RUN###################################################################



