import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.title("📈 株価チャート表示")

# 🧪 開発モード切替
dev_mode = st.sidebar.checkbox("🧪 開発モード（ローカルキャッシュ使用）", value=True)

# 測定範囲
range_option = st.selectbox("📅 測定範囲を選択してください", {
    "5日": "5d",
    "1週間": "7d",
    "1か月": "1mo",
    "3か月": "3mo",
    "半年": "6mo",
    "1年": "1y"
})

# 銘柄一覧
stocks = {
    "7735.T": "SCREENホールディングス",
    "8035.T": "東京エレクトロン",
    "2134.T": "北浜キャピタルパートナーズ",
    "7888.T": "三光合成",
    "4368.T": "扶桑化学工業"
}
selected_code = st.selectbox("📌 銘柄を選択", list(stocks.keys()), format_func=lambda x: stocks[x])

# ✅ 本番モード：Streamlitのキャッシュ機能
@st.cache_data(ttl=3600)
def load_data_production(code: str, period: str) -> pd.DataFrame:
    df = yf.download(code, period=period, interval="1d")
    if not df.empty:
        df.reset_index(inplace=True)
    return df

# 🧪 開発モード：ローカルファイルを使ったキャッシュ
def load_data_dev(code: str, period: str) -> pd.DataFrame:
    filename = f"cache_{code}_{period}.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename, parse_dates=["Date"])
    else:
        df = yf.download(code, period=period, interval="1d")
        if not df.empty:
            df.reset_index(inplace=True)
            df.to_csv(filename, index=False)
    return df

# 切り替えによってロード方法を変更
if dev_mode:
    df = load_data_dev(selected_code, range_option)
else:
    df = load_data_production(selected_code, range_option)

# データが取れていない場合の処理
if df.empty:
    st.error("⚠️ データの取得に失敗しました。後ほど再試行してください。")
else:
    st.subheader(f"📊 {stocks[selected_code]}（{range_option}）の株価チャート")
    fig = px.line(df, x="Date", y="Close", title=f"{stocks[selected_code]} 株価推移")
    st.plotly_chart(fig, use_container_width=True)


#ニュースの取得
import feedparser
from datetime import datetime
import hashlib

def get_company_name_from_code(code):
    return stocks.get(code, code)

def news_cache_filename(company_name):
    hash_name = hashlib.md5(company_name.encode()).hexdigest()
    return f"news_{hash_name}.csv"

def fetch_and_cache_news(company_name, max_items=10):
    rss_url = f"https://news.google.com/rss/search?q={company_name}+株価&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(rss_url)
    items = []
    for entry in feed.entries[:max_items]:
        published = entry.get("published", "")[:16]  # 日付だけ
        items.append({
            "title": entry.title,
            "link": entry.link,
            "published": published
        })
    df = pd.DataFrame(items)
    df.to_csv(news_cache_filename(company_name), index=False)
    return df

def load_news(company_name):
    cache_file = news_cache_filename(company_name)
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
    else:
        df = fetch_and_cache_news(company_name)
    return df

# 🚀 ニュース取得＋表示
company_name = get_company_name_from_code(selected_code)
news_df = load_news(company_name)

st.subheader(f"📰 {company_name} に関する最新ニュース")
if news_df.empty:
    st.write("ニュースが見つかりませんでした。")
else:
    for _, row in news_df.iterrows():
        st.markdown(f"- [{row['published']} 📅] [{row['title']}]({row['link']})")
