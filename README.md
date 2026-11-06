<img width="571" height="324" alt="BookScout-run" src="https://github.com/user-attachments/assets/b9724700-2ae8-41aa-932b-0c5bcd3d83b6" /># BookScout

A Python scraper for [Books to Scrape](https://books.toscrape.com/). Enter how many pages to scrape, a maximum price, and a minimum rating. It compares sequential and concurrent scraping, then prints the cheapest matching books.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests beautifulsoup4
python scraper.py
```

Press Enter to use the defaults: 10 pages, £20 maximum, and at least 4 stars. With one page, the program only runs sequentially.

## Performance

`map` turns book cards into dictionaries. `filter` keeps matching books, and `sorted` orders them by price. Both modes use the same parsing function; the difference is how the requests are scheduled.

`ThreadPoolExecutor.map` fetches pages with up to four workers. Requests can overlap while waiting for the website to respond.

One run with 10 pages returned the same 200 books in both modes:

| Mode | Time |
| --- | ---: |
| Sequential | 6.744 s |
| Concurrent | 1.659 s |

## Screenshot
<img width="571" height="324" alt="BookScout-run" src="https://github.com/user-attachments/assets/1afc0a30-956f-40eb-8e4f-332c4a041a34" />
