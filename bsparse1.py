import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()
def get(url):
    try:
        return requests.get(url,headers={'User-Agent':ua.random})
    except Exception as e:
        print(e,'passing..')
        pass
response = get('http://192.168.86.115/mutillidae/index.php?page=dns-lookup.php')
bsparse = BeautifulSoup(response.content,"html.parser")
forms = bsparse.findAll('form')
for form in forms:
    print(forms)