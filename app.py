import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
import urllib.parse

# 銘柄リストと名称
stocks = {
    "7735.T": "SCREEN HD",
    "8035.T": "東京エレクトロン",
    "2134.T": "北浜キャピタルP",
    "7888.T": "三光合成",
    "4368.T": "扶桑化学工業"
}

# 材料判定キーワード
good_keywords = ["増益", "黒字", "上方修正", "提携", "買収", "新工場", "好調"]
bad_keywords = ["減益", "赤字", "下方修正", "リコール", "不祥事", "訴訟", "値下げ"]

def classify_news(title):
    if any(k in title for k in good_keywords):
        return "好材料"
    elif any(k in title for k in bad_keywords):
        return "悪材料"
    else:
        return "中立"

def get_news(keyword, max_results=5):
    encoded_keyword = urllib.parse.quote(keyword + " 株価")
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(url)
    return [(entry.title, entry.published) for entry in feed.entries[:max_results]]

def get_stock_price_trend(code):
    try:
        df = yf.download(code, period="7d", progress=False)
        return "📈 上昇傾向" if df["Close"][-1] > df["Close"][0] else "📉 下落傾向"
    except:
        return "—"

st.title("株ニュース自動仕分け＆銘柄絞り込み")

selected_code = st.selectbox("銘柄を選択してください", list(stocks.keys()), format_func=lambda x: stocks[x])

if st.button("ニュース取得・判定開始"):
    trend = get_stock_price_trend(selected_code)
    news_list = get_news(stocks[selected_code])

    results = []
    for title, date in news_list:
        label = classify_news(title)
        results.append({"日付": date, "ニュース見出し": title, "材料判定": label})

    df = pd.DataFrame(results)
    df["日付"] = pd.to_datetime(df["日付"], format="mixed")
    df = df.sort_values("日付", ascending=False).reset_index(drop=True)

    st.write(f"### {stocks[selected_code]} の株価傾向: {trend}")
    st.markdown("#### ニュース一覧（折り返し表示）")

    st.markdown(
        df.style.set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'left')]},
            {'selector': 'td', 'props': [('text-align', 'left'), ('white-space', 'normal')]}
        ]).hide(axis='index').to_html(escape=False),
        unsafe_allow_html=True
    )