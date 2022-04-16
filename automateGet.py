import requests, re
def getRequest():
    import requests

    cookies = {
    '_learn_press_session_a6dd6ba6ff5d4b813ae004e5a9eab2ca': '84a86b973ee078cd5239347d2e976b14%7C%7C1650146618%7C%7Cd18df1d49472e6f1e53a5a844df67ec9',
    'PHPSESSID': '5hb58brp622h1rst7p36hv68bq',
    '_gcl_au': '1.1.2017161591.1649973824',
    }

    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_learn_press_session_a6dd6ba6ff5d4b813ae004e5a9eab2ca=84a86b973ee078cd5239347d2e976b14%7C%7C1650146618%7C%7Cd18df1d49472e6f1e53a5a844df67ec9; PHPSESSID=5hb58brp622h1rst7p36hv68bq; _gcl_au=1.1.2017161591.1649973824',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }

    response = requests.get('https://zsecurity.org/', headers=headers, cookies=cookies)
    return response.content

def getLinks(get): #getLinks uses Crawler get() method
    returnLinks = []
    
    #print(type(content))
    #with open('content.txt','w') as wf:
    #wf.write(str(response))
    #print(content)
    #print(type(content))
    hrefs = re.findall(b'(?:href=")(.*?)"',get)
    for href in hrefs:
        if b'div' not in href:
            returnLinks.append(href)
    return returnLinks
print(getLinks(getRequest()))
#print(getRequest())


#used copy as curl with firefox in network tab, paste to curlconvert.com with python amd spits out the dictionaries to use  