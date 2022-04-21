import re, requests, time
from fake_useragent import UserAgent
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from selenium import webdriver
ua = UserAgent()

def parseLinks(get):
	if isinstance(get,bytes):
		try:
			get = get.decode()
		except:
			get = str(get)
	
	return re.findall('(?:href=")(.*?)"',get)

def crawlerSel(url):
	parsedLinks = parseLinks(selGet(url))

	for link in parsedLinks:
		if not link.endswith('feed/'):
			if 'http' or 'https' not in link:
				link = urljoin(url,link)
			
			if '#' in link:
				link = link.split('#')[0]

			if url in link and link not in storeLinks:
				storeLinks.append(link)
				print(link)
				try:
					crawlerSel(link)
				except:
					print(f'\nCould not extract links from {link}\n')
					pass
		else:
			if link not in storeLinks:
				storeLinks.append(link)
				print(link)

def crawlerReq(url):
	parsedLinks = parseLinks(reqGet(url))
	#print(parsedLinks)
	
	for link in parsedLinks:	
		
		if 'http' or 'https' not in link:
			link = urljoin(url,link)
			#print(f'link joined: {link}')
		
		if '#' in link:
			link = link.split('#')[0]
   

		if url in link and link not in storeLinks:
			storeLinks.append(link)
			print(link)
			try:
				crawlerReq(link)
			except:
				print(f'Could not extracxt links from {link}')
				pass

def extract(url):
    get = requests.get(url)
    return re.findall('(?:href=")(.*?)"',str(get.content))

def crawl(url):
    href_links = extract(url)
    #print(f'href from {url}\n\n{href_links}')
    
    for link in href_links:
        link = urljoin(url,link)
        #print(link)
        if '#' in link:
            link = link.split('#')[0]
        if url in link and link not in temp:
            temp.append(link)
            print(link)
            crawl(link)
        
def crawlerBase(url):
    while True:
        checkType = input('Enter sel for selenium or req for requests')
        if checkType == 'sel' or 'req':
            break
    if checkType == 'sel':
    	parsedLinks = parseLinks(selGet(url))
    elif checkType == 'req':
        parsedLinks = parseLinks(reqGet(url))
    links = []
    for link in parseLinks(selGet(url)):
        if 'http' or 'https' not in link:
            link = urljoin(url,link)
        if '#' in link:
            link = link.split('#')[0]
        if url in link and link not in links:
            print(link)
            
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

def reqGet(url):
	headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
	response = requests.get(url,headers = headers)
	if response:		
		return response.content

def gethtmlLib(url):
	page = urllib.request.Request(url,headers=headers)
	page = Request(url,headers=headers)
	webpage = urlopen(page).read()
	print(webpage.decode(""))

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



########################################################RUN###################################################################

storeLinks = []
crawlerSel('https://zsecurity.org')
