import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from pathlib import Path

URL = "https://www.amazon.com/best-sellers-books-Amazon/zgbs/books"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
}

def scrape_books(limit=20):
    r = requests.get(URL, headers=headers, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    books = []
    for item in soup.select(".zg-grid-general-faceout")[:limit]:
        title = item.select_one(".p13n-sc-truncate") or item.select_one("._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y")
        author = item.select_one(".a-row.a-size-small")
        link = item.select_one("a.a-link-normal")

        books.append({
            "title": title.get_text(strip=True) if title else None,
            "author": author.get_text(strip=True) if author else None,
            "url": f"https://www.amazon.com{link['href']}" if link else None
        })
    return books

if __name__ == "__main__":
    Path("data").mkdir(exist_ok=True)
    today = str(date.today())
    books = scrape_books()

    with open(f"data/{today}.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    with open("data/latest.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(books)} books for {today}")
