import feedparser
import csv
from datetime import datetime, timedelta
import os
from tickers import TICKERS

# ニュース収集対象の銘柄（TICKERS から生成、キーワード対応は前提）
TARGETS = []
for code, info in TICKERS.items():
    TARGETS.append({
        "code": code.replace(".T", ""),
        "name": info["name"],
        "keywords": [info["name"]] + info.get("keywords", [])
    })

# 保存ファイルパス
SAVE_PATH = "data/news_history.csv"

# GoogleニュースRSS銘柄別URLを作成
def build_google_news_rss_urls(targets):
    base_url = "https://news.google.com/rss/search?q="
    urls = []
    for target in targets:
        query = "+OR+".join(target["keywords"])
        # URLエンコードが必要な場合は urllib.parse.quote_plus を使ってください
        urls.append(f"{base_url}{query}&hl=ja&gl=JP&ceid=JP:ja")
    return urls

RSS_FEEDS = build_google_news_rss_urls(TARGETS)

# 過去何日分のニュースを収集するか
DAYS_BACK = 30


def fetch_news():
    news_entries = []
    since_date = datetime.now() - timedelta(days=DAYS_BACK)

    for feed_url in RSS_FEEDS:
        print(f"読み込み中のRSS: {feed_url}")
        feed = feedparser.parse(feed_url)
        print(f"エントリ数: {len(feed.entries)}")

        for entry in feed.entries:
            if 'published_parsed' not in entry:
                continue
            published = datetime(*entry.published_parsed[:6])
            if published < since_date:
                continue

            title_lower = entry.title.lower()

            for target in TARGETS:
                keywords_lower = [kw.lower() for kw in target["keywords"]]
                if any(kw in title_lower for kw in keywords_lower):
                    news_entries.append({
                        "date": published.strftime("%Y-%m-%d"),
                        "code": target["code"],
                        "title": entry.title,
                        "summary": entry.get("summary", ""),
                        "url": entry.link
                    })
                    break

    return news_entries


def save_news_to_csv(news_entries):
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "code", "title", "summary", "url"])
        writer.writeheader()
        writer.writerows(news_entries)


if __name__ == "__main__":
    print("ニュース収集中...")
    entries = fetch_news()
    save_news_to_csv(entries)
    print(f"{len(entries)} 件のニュースを保存しました → {SAVE_PATH}")
