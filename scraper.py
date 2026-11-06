from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

from bs4 import BeautifulSoup
import requests

BASE_URL = "https://books.toscrape.com/"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_book(card):
    return {
        "title": card.select_one("h3 a")["title"],
        "price": float(card.select_one(".price_color").text.replace("£", "")),
        "rating": RATINGS[card.select_one(".star-rating")["class"][1]],
    }


def fetch_page(url):
    with requests.get(url, timeout=15) as response:
        response.raise_for_status()
        cards = BeautifulSoup(response.content, "html.parser").select("article.product_pod")
        if not cards:
            raise ValueError(f"No books found on {url}")
        return list(map(parse_book, cards))


def scrape(urls, workers):
    if workers == 1:
        pages = list(map(fetch_page, urls))
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pages = list(pool.map(fetch_page, urls))
    return [book for page in pages for book in page]


def main():
    pages = int(input("Pages to scrape [10]: ") or "10")
    max_price = float(input("Maximum price in GBP [20]: ") or "20")
    min_rating = int(input("Minimum rating, 1-5 [4]: ") or "4")
    if not 1 <= pages <= 50 or not 1 <= min_rating <= 5:
        raise ValueError("Choose 1-50 pages and a rating from 1 to 5.")
    urls = [BASE_URL] + [f"{BASE_URL}catalogue/page-{n}.html" for n in range(2, pages + 1)]
    times, results = [], []
    modes = [("Sequential", 1)]
    if pages > 1:
        modes.append(("Concurrent", min(4, pages)))
    for name, workers in modes:
        print(f"\n{name}: fetching {pages} pages with {workers} worker(s)...", flush=True)
        started = perf_counter()
        books = scrape(urls, workers)
        elapsed = perf_counter() - started
        times.append(elapsed)
        results.append(books)
        print(f"{len(books)} books in {elapsed:.3f} seconds")

    if pages > 1:
        if results[0] != results[1]:
            raise ValueError("Book data changed between runs. Try again.")
        print(f"\nSame results. Speedup: {times[0] / times[1]:.2f}x")
    selected = filter(lambda book: book["price"] <= max_price and book["rating"] >= min_rating, books)
    selected = sorted(selected, key=lambda book: book["price"])
    print(f"\n{len(selected)} books match. Showing up to 8, cheapest first:")
    for book in selected[:8]:
        print(f'£{book["price"]:.2f} | {book["rating"]}/5 | {book["title"]}')


if __name__ == "__main__":
    main()
