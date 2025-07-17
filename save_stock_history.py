import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# 対象銘柄リスト（拡張可能）
TICKERS = {
    "7735.T": "SCREENホールディングス",
    "8035.T": "東京エレクトロン",
    "2134.T": "北浜キャピタルパートナーズ",
    "7888.T": "三光合成",
    "4368.T": "扶桑化学工業"
}

SAVE_DIR = "data"
os.makedirs(SAVE_DIR, exist_ok=True)

# 期間指定（例：過去60営業日程度）
PERIOD = "3mo"  # or "60d"

def save_stock_data(ticker):
    df = yf.download(ticker, period=PERIOD, interval="1d", progress=False)
    df.reset_index(inplace=True)
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

    save_path = os.path.join(SAVE_DIR, f"{ticker}.csv")
    df.to_csv(save_path, index=False)
    print(f"✅ {ticker} のデータ保存完了: {save_path}")

if __name__ == "__main__":
    for ticker in TICKERS:
        save_stock_data(ticker)
