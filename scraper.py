import requests
import json
from datetime import date
from pathlib import Path

# 👉 替换成你的 RapidAPI key
RAPIDAPI_KEY = "37a8eb5dffmsh072d63ab576f67dp14657bjsn67dfcedf4352"

# RapidAPI 配置
RAPIDAPI_HOST = "realtime-amazon-data.p.rapidapi.com"
BESTSELLERS_ENDPOINT = f"https://{RAPIDAPI_HOST}/best-sellers"

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

def fetch_bestsellers(category="books", country="US", limit=20):
    """调用 RapidAPI 获取亚马逊畅销榜"""
    params = {"category": category, "country": country}
    r = requests.get(BESTSELLERS_ENDPOINT, headers=headers, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()

    print('data.json:',data)
    
    items = []
    for i, book in enumerate(data.get("products", [])[:limit], 1):
        items.append({
            "rank": book.get('rank'),
            "title": book.get("title"),
            "img": book.get("imageUrl"),
            "url": book.get("link"),
            "price": book.get("price"),
            "rating": book.get("rating")
        })
    return items

if __name__ == "__main__":
    Path("data").mkdir(exist_ok=True)
    today = str(date.today())

    books = fetch_bestsellers(limit=20)

    # 保存每日快照
    with open(f"data/{today}.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    # 保存 latest.json
    with open("data/latest.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(books)} books for {today}")
