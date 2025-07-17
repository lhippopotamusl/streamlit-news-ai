from tickers import TICKERS
from datetime import datetime
import pandas as pd
import os

def dummy_news_fetch(ticker):
    # 実際はAPI連携 or RSS取得に差し替え予定
    return [
        {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "ticker": ticker,
            "headline": f"{ticker} に関する重要なニュース",
            "summary": "概要はここに",
            "keyword": "dummy",
            "source": "DummyNews"
        }
    ]

def save_news_data():
    all_news = []
    for code in TICKERS.keys():
        news_items = dummy_news_fetch(code)
        all_news.extend(news_items)

    df = pd.DataFrame(all_news)
    os.makedirs("data", exist_ok=True)
    path = "data/news_data.csv"

    try:
        existing_df = pd.read_csv(path)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.drop_duplicates(subset=["date", "ticker", "headline"], inplace=True)
    except FileNotFoundError:
        combined_df = df

    combined_df.to_csv(path, index=False)
    print(f"📰 ニュースデータ保存完了: {path}")

if __name__ == "__main__":
    save_news_data()
