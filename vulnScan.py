from spider import Spider
from bs4 import BeautifulSoup
import argparse

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
		self.storeLinks = spider.storeLinks

	def listLinks(self,lst):
		spider.run()
		self.storeLinks = self.spider.storeLinks # not sure how to do this best, would want to pass the list straight to the method, call spider.run seperate
		for link in lst:
			print(link)
	
	def postData(self):
		html = self.spider.reqGet(self.url)
		bsparse = BeautifulSoup(html,"html.parser")
		postData = {}
		print(bsparse)
	





#########################################################RUN#######################################################



args = Args()
v1 = Vulnscan(args.url)
#v1.listLinks(v1.storeLinks)
v1.postData()



