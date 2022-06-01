import requests, argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
ua = UserAgent()

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--URL',dest='url',help='Enter target URL.')
    options = parser.parse_args()
    return options
    
def get(url):
    try:
        resp = requests.get(url,headers={'User-Agent':ua.random})
        if resp.status_code == 200:
            return resp.content
        else:
            return None
    except Exception as e:
        print(e,'passing..')
        pass

def parse(url):
    response = get(url)
    counter = 1
    if response != None:
        bsparse = BeautifulSoup(response,"html.parser")
        forms = bsparse.findAll('form')
        for form in forms:
            action = form.get('action')
            fullurl = (urljoin(url, action))
            method = form.get('method')
            print(f'Relative url: {action}')
            print(f'Joined url: {fullurl}')
            print(f'Method: {method}')
            inputList = form.findAll('input')
            postData = {}
            for i in inputList:
                print(f'Input {counter}: {i}')
                inputName = i.get('name')
                inputType = i.get('type')
                inputValue = i.get('value')
                if inputType == 'text':
                    inputValue = 'test'
                postData[inputName] = inputValue
                counter += 1
            result = requests.post(fullurl,data = postData)
            bsPage = (BeautifulSoup(result.content,'html.parser'))
            print(bsPage.findAll('p'))
            
args=args()                    
parse(args.url)
