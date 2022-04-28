from spider import Spider
import argparse

class Args:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-u','--url',dest = 'url', help = 'Enter target URL.')     
        options = parser.parse_args()
        self.url = options.url
        

class Vulnscan:
	def __init__(self,url):
		spider = Spider(url)
		spider.run()
		self.storeLinks = spider.storeLinks
		#print(f'storeLinks: \n\n{self.storeLinks}')

	def listLinks(self,lst):
		for link in lst:
			print(link)





#########################################################RUN#######################################################



args = Args()
v1 = Vulnscan(args.url)
v1.listLinks(v1.storeLinks)


