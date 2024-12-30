from bs4 import BeautifulSoup
import requests

page_to_scrape = requests.get("https://quotes.toscrape.com").text
soup = BeautifulSoup(page_to_scrape, "html.parser")

quotes = soup.find_all("span", attrs={"class": "text"})
authors = soup.find_all("small", attrs={"class": "author"})

parent=authors[0].parent
a = parent.find('a')
a.string = "about"
print(a.string)

# for quote, author in zip(quotes, authors):
#     print(f"{quote.text} by {author.text} \n\n")