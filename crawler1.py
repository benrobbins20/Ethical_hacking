import requests

class Crawler:
    def __init__(self,url):
        self.url = url
    def get(self,testurl):
        try:
            #print(requests.get(testurl))
            return requests.get(f'http://{testurl}',timeout=.1)
        except Exception as e:
            #print(f'Error Connecting to {testurl}, trying next')
            pass
    def subdomains(self):
        with open('/root/Downloads/subdomains.txt','r') as rf:
            for line in rf:
                line = line.strip()
                #print("\r"+line,end='')
                #print(line,end='')
                #print(line)
                self.suburl = f'{line}.{self.url}'
                #print(f'Trying get: {self.suburl}')
                response = self.get(self.suburl)
                if response:
                    print(f'\n{response} >> http://{self.suburl}')
                else:
                    print(f'\r{line}                             ',end="")

################################################################RUN######################################################################

crawler = Crawler("google.com")
crawler.subdomains()

    