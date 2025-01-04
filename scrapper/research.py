from bs4 import BeautifulSoup
import requests 


url = ["https://arxiv.org/list/cs.SE/recent", "https://arxiv.org/list/cs.LG/recent", "https://paperswithcode.com/"]

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")

header = doc.find('h1')
dates = doc.find('h3')
items = doc.find_all('a', {'name': True}, limit=5)
itmes_abstract = doc.find('a', {"title": "Abstract"})


print(itmes_abstract.get('href'))

request_details = requests.get("https://arxiv.org/" + itmes_abstract.get('href'))
doc_details = BeautifulSoup(request_details.text, "html.parser")

header = doc_details.find('h1', {'class': 'title mathjax'})
print(header.text)
description = doc_details.find('blockquote')
print(description.text)



for item in items:
    print(item.text)
print(header.text)