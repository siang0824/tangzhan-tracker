import os
import re
import requests
from datetime import datetime

BOOKING_URL = "https://inline.app/booking/-LLj4E2uNTYeHQKcDmre:inline-live-2a466/-LLj4EBLorSlhI14L7r9?language=zh-tw"
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)

def get_latest_date():
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Accept-Language": "zh-TW,zh;q=0.9",
    }
    try:
        r = requests.get(BOOKING_URL, headers=headers, timeout=20)
        dates = sorted(set(re.findall(r"20\d{2}-\d{2}-\d{2}", r.text)))
        return dates[-1] if dates else None
    except Exception as e:
        print("Error:", e)
        return None

latest = get_latest_date()
print("Latest date:", latest)

if latest:
    send_msg(f"湯棧目前最遠可訂日期：{latest}\n{BOOKING_URL}")
else:
    send_msg("目前無法取得湯棧可訂日期（可能被擋或尚未開放）")
