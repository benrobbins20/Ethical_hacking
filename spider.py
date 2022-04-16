from crawler2 import Crawler
import re, requests
#from fake_useragent import UserAgent
from urllib.request import Request, urlopen
#ua = UserAgent()
hdrs = {
	'Host': 'zsecurity.org',
	'Referer': 'https://www.google.com/',
	'User-Agent': "Chrome/100.0.4896.88",
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate, br',
	'DNT': '1',
	'Upgrade-Insecure-Requests': '1',
	'Connection': 'keep-alive',
	'Sec-Fetch-Dest': 'document',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-Site': 'none',
	'Sec-Fetch-User': '?1',
	}
#GET / HTTP/3
#Host: zsecurity.org
#User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
#Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
#Accept-Language: en-US,en;q=0.5
#Accept-Encoding: gzip, deflate, br
#DNT: 1
#Connection: keep-alive
#Cookie: _learn_press_session_a6dd6ba6ff5d4b813ae004e5a9eab2ca=ea95b40d06dfa8db35cf76afc414ad1c%7C%7C1650132223%7C%7C4ff1338be3d2fb1a4bc529f8f2ef42f7; PHPSESSID=8m0evj368sjq82oi53l64mp1vl; _gcl_au=1.1.230257486.1649959431
#Upgrade-Insecure-Requests: 1
#Sec-Fetch-Dest: document
#Sec-Fetch-Mode: navigate
#Sec-Fetch-Site: none
#Sec-Fetch-User: ?1

def getLinks(get): #getLinks uses Crawler get() method
	returnLinks = []
	if get:
		content = get.content
		#print(type(content))
		#with open('content.txt','w') as wf:
		#wf.write(str(response))
		#print(content)
		#print(type(content))
		hrefs = re.findall(b'(?:href=")(.*?)"',content)
		for href in hrefs:
			if b'div' not in href:
				returnLinks.append(href)
		return returnLinks

def geturlLinks(url): #using requests in func
	#{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}
	#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0'}
	#headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}
	#headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}
	#headers = {'Accept-Language': 'en-US;q=0.7,en;q=0.3'}
	headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}
	response = requests.get(url,headers=headers)
	print(response)
	returnLinks = []
	if response:
		if response == 200: # sanity check
			print(response,'STATUS CODE')
		hrefs = re.findall(b'(?:href=")(.*?)"',response.content)
		for href in hrefs:
			if b'div' not in href:
				returnLinks.append(href)
		return returnLinks
def gethtml(url):
	#headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
	response = requests.get(url,headers = hdrs)
	if response:
		if response == 200: # sanity check
			print(response,'STATUS CODE')
		
		return response.content

def gethtmlLib(url):
	page = urllib.request.Request(url,headers=headers)
	page = Request(url,headers=headers)
	webpage = urlopen(page).read()
	print(webpage.decode(""))

	#infile=urllib.request.urlopen(page).read()
	#print(infile[0:50])
	#data = infile.decode()
	#print(data)
	#return infile.decode()




#c2 = Crawler('reddit.com')
#print(getLinks(c2.get()))
#print(geturlLinks("http://webcache.googleusercontent.com/search?q=cache:www.zsecurity.org"))
#print(gethtml("http://webcache.googleusercontent.com/search?q=cache:www.zsecurity.org")) #kind of interesting to see cache data, not real time so not ideal for scraping
print(gethtml('https://zsecurity.org/'))
#print(gethtmlLib("http://zsecurity.org"))

