import brotli, re
from urllib.request import Request, urlopen
headers = {
    'authority': 'zsecurity.org',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://zsecurity.org/',
    'accept-language': 'en-US,en;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_fbp=fb.1.1650136152747.1037171996; _learn_press_session_a6dd6ba6ff5d4b813ae004e5a9eab2ca=5c0f60c908bd644bdf54daff03898936%7C%7C1650308952%7C%7Ce37869b870c518899763f1c2d834a9a9; PHPSESSID=vts00iq6nvf2a0tt423lshvj0u; _gcl_au=1.1.852979028.1650136156; _ga=GA1.2.496462929.1650136156; _gid=GA1.2.1857317549.1650136156; _gat_gtag_UA_165947000=1; moove_gdpr_popup=%7B%22strict%22%3A%221%22%2C%22thirdparty%22%3A%221%22%2C%22advanced%22%3A%221%22%7D; wordpress_test_cookie=WP%20Cookie%20check; pmpro_visit=1; wordpress_logged_in_a6dd6ba6ff5d4b813ae004e5a9eab2ca=thehitmonkey%7C1650308982%7CsPOjm95Pxs0eZi9s7GMvomRmwoltPKBWFAyHw2qqK3J%7Cf1f63f317c660d64177534f8d463137b9504aedd39101e357179ac1861041e36; __stripe_mid=70280fc3-6e24-4eec-bd0f-049de7a4d633848660; __stripe_sid=4a9aa528-fa8d-441a-9c2c-89c6d33fd2b586d9e2',
}
def gethtmlLib(url):
	#page = urllib.request.Request(url,headers=headers)
	page = Request(url,headers=headers)
	webpage = urlopen(page).read()
	return webpage
def geturlLinks(webpage):
    returnLinks = []
    hrefs = re.findall('(?:href=")(.*?)"',str(webpage))
    for href in hrefs:
        if 'div' not in href:
            returnLinks.append(href)
    return returnLinks

lst = (geturlLinks(gethtmlLib('http://zsecurity.org')))
# print(len(lst))
for lst in lst:
    print(lst)
    print('\n')