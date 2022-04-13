import requests, threading, sys
class fc: #ascii font color class
    rw = '\033[31;107m'
    r = '\033[38;5;196m'
    pv = '\033[38;5;206;48;5;57m'
    end = '\033[0m'
    pink = '\033[38;5;206m'
    y = '\033[0;33;40m'
    purple = '\033[0;35m'
    wg = '\033[37;42m'
    cyan = '\033[36m'
    g = '\033[38;5;154m'
    b = '\033[38;5;45m'

class Crawler:
    
    def __init__(self,url):
        self.url = url
    
    def get(self,testurl=None):
        if testurl == None:
            testurl = self.url
        try:
            #print(requests.get(testurl))
            return requests.get(f'http://{testurl}',timeout=.1)
        except Exception as e:
            #print(f'Error Connecting to {testurl}, trying next')
            pass
    
    def subdomains(self):
        with open('/opt/wordlists/subdomains.txt','r') as rf:
            for line in rf:
                line = line.strip()
                #print("\r"+line,end='')
                #print(line,end='')
                #print(line)
                suburl = f'{line}.{self.url}'
                #print(f'Trying get: {self.suburl}')
                response = self.get(suburl)
                if response:
                    print(f'{fc.wg}\n{response} >> http://{self.suburl}{fc.end}')
                else:
                    print(f'{fc.rw}\r{line}{fc.end}                             ',end="")
    
    def directories(self):
        with open('/opt/wordlists/common.txt','r') as rf:
            for line in rf:
                line = line.strip()
                dirurl = f'{self.url}/{line}'
                #print(f'\r{dirurl}                             ',end="")
                #print(dirurl) #google.com/testdir
                response = self.get(dirurl) 
                if response:
                    print(f'{fc.g}\n{response} >> http://{dirurl}{fc.end}')
                else:
                    print(f'{fc.r}\r{line}{fc.end}                             ',end="")

################################################################RUN######################################################################


try:
    crawler = Crawler("<IPorDomainName>")
    subdomainThread = threading.Thread(target=crawler.subdomains)
    #crawler.subdomains()
    directoryThread = threading.Thread(target=crawler.directories)
    #crawler.directories()
    subdomainThread.start()
    directoryThread.start()

except KeyboardInterrupt:
    #subdomainThread.join() # not cracefully exiting for some reason, gets execution halted during requests or threading?
    #directoryThread.join()
    sys.exit()
except Exception as e:
    print(f'{fc.rw}Error: {e}{fc.end}\n{fc.rw}{traceback.format_exc()}{fc.end}')