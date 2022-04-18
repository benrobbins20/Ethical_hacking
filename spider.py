import re, requests
from fake_useragent import UserAgent
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from zsecHeaders import zsecurityResponse
#print(zsecurityResponse)
from selenium import webdriver
ua = UserAgent()

def parseLinks(baseurl,get): #function will not use requests, import headers from another file, pass get.content into function
	if isinstance(get,bytes):
		try:
			get = get.decode()
		except:
			get = str(get)

	#print(f'Get test: {get[0:50]}\t\t{type(get)}')
	links = []
	hrefs = re.findall('(?:href=")(.*?)"',get)
	for link in hrefs:
		if 'http' or 'https' not in link:
			link = urljoin(baseurl,link) 
			if baseurl in link:
				links.append(link)
	return links

def geturlLinks(url): #using requests in func
	response = requests.get(url,headers={'User-Agent':ua.random})
	print(f'Status code: {response.status_code}')
	returnLinks = []
	fullLink = []
	if response:	
		hrefs = re.findall('(?:href=")(.*?)"',str(response.content))
		for href in hrefs:
			#if b'div' not in href:
			returnLinks.append(href)
	for link in returnLinks:
		link = urljoin(url,link)
		fullLink.append(link)
	return fullLink
		#return returnLinks

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

def selGet(url):
	fireFoxOptions = webdriver.FirefoxOptions()
	#print(dir(fireFoxOptions))
	fireFoxOptions.headless = True
	brower = webdriver.Firefox(options = fireFoxOptions)
	brower.get(url)
	return (brower.page_source)# when requests or urllib does not work, can run selenium headless to get page source

def lstLinks(lst):
	for link in lst:
		print(link)

########################################################EXAMPLES###############################################################

#lst = (geturlLinks("http://chegg.com"))
#lst = parseLinks("http://zsecurity.org",selGet("http://zsecurity.org"))
#lst = (geturlLinks("http://192.168.86.115/mutillidae"))


########################################################RUN###################################################################

lst = parseLinks("https://zsecurity.org",selGet("https://zsecurity.org"))
lstLinks(lst)