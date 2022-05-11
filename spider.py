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
		self.fuckedList = []
		
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
		else:
			return None
		
	def postForm(self,forms,value,url): # can pass a list in for forms but should only be 1 item
		#try:
		print('postForm\n')
		for form in forms:
			inputList = form.findAll('input')
			postData = {}
			action = form.get('action')
			fullurl = (urljoin(url, action))
			method = form.get('method')
			# print(
			# f'\n{fc.p}Link: {fullurl}{fc.end}\n'
			# f'{fc.p}Action: {action}{fc.end}\n'
			# f'{fc.p}Method: {method}{fc.end}\n'
			# f'{fc.p}Inputs: {inputList}{fc.end}\n'
			# )
			if inputList:
				for i in inputList:
					inputName = i.get('name')
					inputType = i.get('type')
					inputValue = i.get('value')
					if inputType == 'text':
						inputValue = value
					postData[inputName] = inputValue
					#print(f'Post Data: {postData}')
					if method == 'post':
						print('Sending Post')
						return self.session.post(fullurl,data=postData)
					print('Sending get')
					return self.session.get(fullurl,params=postData)
			else:
				print(f'{fc.r}No inputs found on {fullurl}{fc.end}')
				return None
	    
	def runScan(self):
		for link in self.storeLinks:
			forms = self.getForms(link)
			if forms:
				print(f'{fc.pu}-{fc.end}'*50)
				print(f'\n{fc.pv}[+]{fc.end} Discovering vulnerability for {fc.cy}{link}{fc.end}')
				
				
					#print(f'{fc.pv}[+]{fc.end} {fc.g}XSS found at{fc.end} {fc.cy}{link}{fc.end}\nForm:\n\n{fc.pu}{forms}{fc.end}\n\n')
			# if '=' in link:
			# 	print(f'{fc.pv}[+]{fc.end} Testing {fc.cy}{link}{fc.end}')
			# 	is_vulnerable = self.testXSS(link)
			# 	if is_vulnerable:
			# 		print(f'{fc.pv}[+]{fc.end} {fc.g}XSS found at{fc.end} {fc.cy}{url}{fc.end}\nForm:\n\n{fc.pu}{form}{fc.end}\n\n')
			else:
				print(f'{fc.pu}-{fc.end}'*50)
				print(f'{fc.r}No forms in {link}{fc.end}')
	
	def bruteRun(self):
		testScript = '<sCript>alert("test")</scriPt>'
		for link in self.fuckedList:
			forms = self.getForms(link)
			response = self.postForm(forms,testScript,link)
			print(testScript in response.text,'\n',link)
			print(response.text)
	
	def testXSS(self,url,forms=None): #forms can be list
		#print('testXSS\n\n')
		# print(
		# 	f'{fc.rw}TROUBLESHOOT{fc.end}\n'
		# 	f'URL {url}\n'
		# 	f'Form: {fc.cy}{forms}{fc.end}'
		# )
		testScript = '<sCript>alert("test")</scriPt>'
		#print(type(forms)) # bs4 match class not list but can be treated like a list list[0]
		if forms: # makes sure that list is not empty
			#print(type(forms))
			#for form in forms:
				#print(form.findAll('input'))
			response = self.postForm(forms,testScript,url) # postForm can take a list and parse the bs4 object	
			if response:
				if 'Hacking attempt' in str(response.content):
					print('pwned')
					self.fuckedList.append(url)
				else:
					if testScript in str(response.content):
						print(f'{fc.pv}URL{fc.end} {fc.rw}{url}{fc.end} {fc.pv}is vulnerable to XSS!{fc.end}')
						return True
			else:
				print(f'{fc.r}URL >>{fc.end} {fc.cy}{url}{fc.end} {fc.r}is not vulnerable to XSS.{fc.end}\n')
				return False

		else: # this will run when no form is passed into function, create link with link/?input=input
			# print(self.getForms(url))
			#print(type(self.getForms(url)))
			if not url.endswith('/'):
				url = url + '/'
			forms = self.getForms(url)
			if forms:
				if len(forms) == 1:
					form = forms[0]
					inputs = form.findAll('input')
					for i in inputs:
						name = (i.get('name'))
						if name: # should not get the input for the submit button == None
							#print(url)
							testUrl = url + f'?{name}={testScript}'
							print(f'Sending URL: {fc.g}{testUrl}{fc.end}')
							response = self.session.get(testUrl)
							print(f'Status code: {response.status_code}')
							if testScript in str(response.content):
								print(f'{fc.pv}URL{fc.end} {fc.rw}{url}{fc.end} {fc.pv}is vulnerable to XSS!{fc.end}')
								return True
							else:
								print(f'{fc.r}URL >>{fc.end} {fc.cy}{url}{fc.end} {fc.r}is not vulnerable to XSS.{fc.end}')
								return False
			else:
				print(f'{fc.r}URL >>{fc.end} {fc.cy}{url}{fc.end} {fc.r}is not vulnerable to XSS.{fc.end}')
				return False




########################################################RUN###################################################################