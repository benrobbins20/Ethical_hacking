import requests
from crawler2 import Crawler

c2 = Crawler('zsecurity.org')
response = c2.get()
print(response.content)