from spider import Spider
from bs4 import BeautifulSoup
import argparse
import passwordPoster as pp

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

	def listLinks(self,lst):
		self.spider.run()
		self.storeLinks = self.spider.storeLinks # not sure how to do this best, would want to pass the list straight to the method, call spider.run seperate
		for link in lst:
			print(link)
	
	def postData(self):
		html = self.spider.reqGet(self.url)
		bsparse = BeautifulSoup(html,"html.parser")
		postData = {}
		print(bsparse)
	
	def sessionSpider(self,dataDict):
		self.spider.run() #run spider to get spider links
		#print(self.spider.storeLinks)
		for link in self.spider.storeLinks: #for loops to get forms for each each page
			html = self.spider.reqGet(link)
			bsparse = BeautifulSoup(html,"html.parser")
			forms = bsparse.findAll('form')
			if forms:

				print(forms)
	def returnCreds(self,url): #uses post script to get creds
		return pp.post(url)

#########################################################RUN#######################################################

args = Args()
v1 = Vulnscan(args.url)
creds = (v1.returnCreds(args.url))
v1.sessionSpider(creds)

#v1.listLinks(v1.storeLinks)
#v1.postData()



