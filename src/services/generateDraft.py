from bs4 import BeautifulSoup
import requests


url = "https://techcrunch.com/"
url2 = "https://www.technologyreview.com/"

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")


print(doc)