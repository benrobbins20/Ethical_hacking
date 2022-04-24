import re, requests, time, argparse, sys
from fake_useragent import UserAgent
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from selenium import webdriver
ua = UserAgent()

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--URL',dest = 'url', help = 'Enter target URL address')
    options = parser.parse_args()
    return options
    
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
			
			if 'http' not in link or 'https' not in link:
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
	for link in parsedLinks:	
		
		if 'http' not in link and 'https' not in link:
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
				print(f'Could not extract links from {link}')
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
	try:
		response = requests.get(url,headers = {'User-Agent': ua.random})
		if response.status_code == 200:
			return response.content
	except Exception as e:
		print(e)

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
  
def run():
	global storeLinks
	global args
	storeLinks = []
	args = args()
	print(args.url)
	if not args.url.endswith('/'):
		args.url = args.url + '/'
		print(f'Confirm URL: {args.url}')
		while True:
			validateURL = input(f'URL Correct? y/n\n:')
			validateURL = validateURL.lower()
			if validateURL == 'y':
				break
			elif validateURL == 'n':
				print('URL error, Qutting...')
				sys.exit()
	while True:
		runType = input('Enter \'sel\' to use selenium or \'req\' to use reqests\n:')
		if runType == 'sel' or runType == 'req':
			break
	if runType == 'sel':
		crawlerSel(args.url)
	elif runType == 'req':
		crawlerReq(args.url)

########################################################RUN###################################################################

run()
