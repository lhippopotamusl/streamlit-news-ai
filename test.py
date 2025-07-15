import requests
print(requests.__version__)

url = "https://query1.finance.yahoo.com/v8/finance/chart/7735.T"
try:
    r = requests.get(url)
    print(r.status_code)
    print(r.text[:200])  # 先頭200文字だけ表示
except Exception as e:
    print("Error:", e)