import os

import pandas as pd
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com"


def scrape_page(url):

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    quotes = []

    quote_blocks = soup.find_all(
        "div",
        class_="quote"
    )

    for block in quote_blocks:

        quote = block.find(
            "span",
            class_="text"
        )

        author = block.find(
            "small",
            class_="author"
        )

        quotes.append({
            "quote": quote.get_text(strip=True),
            "author": author.get_text(strip=True)
        })

    next_button = soup.find(
        "li",
        class_="next"
    )

    if next_button:

        next_link = next_button.find("a")

        next_url = BASE_URL + next_link["href"]

    else:

        next_url = None

    return quotes, next_url


def main():

    all_quotes = []

    url = BASE_URL

    page = 1

    while url:

        print(f"Scraping page {page}...")

        quotes, url = scrape_page(url)

        all_quotes.extend(quotes)

        page += 1

    df = pd.DataFrame(all_quotes)

    os.makedirs(
        "data",
        exist_ok=True
    )

    output_path = os.path.abspath(
        "data/quotes.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print()
    print("Scraping complete!")
    print("Total quotes:", len(df))
    print("Saved to:")
    print(output_path)


if __name__ == "__main__":
    main()
