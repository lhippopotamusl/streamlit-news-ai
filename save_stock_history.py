import yfinance as yf
import pandas as pd
import os
from datetime import datetime
from tickers import TICKERS

def save_stock_data():
    today = datetime.now().strftime("%Y-%m-%d")
    all_data = []
    for code, name in TICKERS.items():
        df = yf.download(code, period="1mo", interval="1d")
        if df.empty:
            print(f"⚠️ データ取得失敗: {code}")
            continue
        df.reset_index(inplace=True)
        df["ticker"] = code
        df["date"] = df["Date"].dt.strftime("%Y-%m-%d")
        df = df[["date", "ticker", "Open", "High", "Low", "Close", "Volume"]]
        all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)
    os.makedirs("data", exist_ok=True)
    path = "data/stock_data.csv"

    try:
        existing_df = pd.read_csv(path)
        combined_df = pd.concat([existing_df, combined_df], ignore_index=True)
        combined_df.drop_duplicates(subset=["date", "ticker"], inplace=True)
    except FileNotFoundError:
        pass

    combined_df.to_csv(path, index=False)
    print(f"✅ 株価データ保存完了: {path}")

if __name__ == "__main__":
    save_stock_data()
