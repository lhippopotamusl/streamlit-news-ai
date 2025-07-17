import pandas as pd

# 例: ニュースCSV読み込み
news_df = pd.read_csv("data/news_history.csv", parse_dates=["date"])
news_df["code"] = news_df["code"].astype(str).str.strip()

# 例: 株価CSV読み込み（複数銘柄をまとめた形想定）
stock_df = pd.read_csv("data/stock_data.csv", parse_dates=["date"])
stock_df.rename(columns={"ticker": "code"}, inplace=True)
stock_df["code"] = stock_df["code"].str.replace(".T", "", regex=False)
stock_df["code"] = stock_df["code"].astype(str).str.strip()

# マージ前に型整形
stock_df["code"] = stock_df["code"].astype(str).str.strip()
news_df["code"] = news_df["code"].astype(str).str.strip()

# 日付もdatetimeに変換済みと仮定
merged_df = pd.merge(news_df, stock_df, on=["date", "code"], how="inner")

print(f"マージ後の件数: {len(merged_df)}")
print(merged_df.head())

# 銘柄コード表記を統一（newsはコードのみ、stockはコード.Tの可能性も）
# ここではstockのコードから「.T」を外す例
stock_df["code"] = stock_df["code"].str.replace(".T", "", regex=False)

# ニュースと株価を日付・銘柄コードでマージ
merged_df = pd.merge(news_df, stock_df, on=["date", "code"], how="inner")

print(f"マージ後の件数: {len(merged_df)}")
print(merged_df.head())

# これで、ニュースが出た日の株価情報が紐づけられます
