import requests
from bs4 import BeautifulSoup


URL = "https://quotes.toscrape.com/"

response = requests.get(
    URL,
    timeout=10
)

response.raise_for_status()

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

quotes = soup.find_all(
    "span",
    class_="text"
)

print("Number of quotes:", len(quotes))

for quote in quotes:
    print(quote.get_text(strip=True))
