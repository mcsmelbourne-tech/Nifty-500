import streamlit as st
import requests
import os

st.set_page_config(page_title="Top 10 Nifty Screener to Telegram", page_icon="📈", layout="centered")

st.title("📈 Top 10 Nifty Stocks Broadcaster")
st.markdown("Paste your TradingView screener rows below to instantly format and broadcast the **Top 10** to Telegram.")

# Sidebar Settings for Telegram Credentials
st.sidebar.header("Telegram Config")
bot_token = st.sidebar.text_input("Bot Token", type="password", value=os.getenv("TELEGRAM_BOT_TOKEN", ""))
chat_id = st.sidebar.text_input("Chat ID", value=os.getenv("TELEGRAM_CHAT_ID", ""))

def send_telegram(message):
    if not bot_token or not chat_id:
        return {"ok": False, "description": "Missing Bot Token or Chat ID."}
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(url, json=payload)
    return response.json()

# Pre-populated with the top rows from your Nifty screener image
default_data = """MANOGRAPH | Manograph India Limited | 18.09 INR | +20.28%
ALKALI | Alkali Metals Ltd. | 87.66 INR | +19.98%
ANYA | Anya Polytech & Fertilizers | 17.85 INR | +19.00%
KLL | Kaushalya Logistics Ltd. | 32.40 INR | +17.82%
TIMEX | Timex Group India Limited | 714.20 INR | +16.50%
SHIVAMAUTO | Shivam Autotech Limited | 19.42 INR | +16.29%
HATHWAYB | Hathway Bhawani Cable... | 12.00 INR | +15.94%
SAMBHV | Sambhv Steel Tubes Limited | 147.57 INR | +14.32%
AVALON | Avalon Technologies Limited | 2,537.7 INR | +13.48%
TCMLMTD | TCM Limited | 57.00 INR | +11.76%"""

raw_input_data = st.text_area("Paste Screener Rows Here", value=default_data, height=220)

if st.button("🚀 Send Top 10 to Telegram"):
    if not raw_input_data.strip():
        st.warning("Please provide stock data.")
    else:
        # Split lines and ensure we slice strictly the top 10
        lines = [line.strip() for line in raw_input_data.strip().split("\n") if line.strip()]
        top_10 = lines[:10]
        
        # Format lines with ranking numbers (1 to 10)
        formatted_lines = []
        for idx, line in enumerate(top_10, 1):
            formatted_lines.append(f"<b>{idx}.</b> <code>{line}</code>")
        
        message = (
            "🚨 <b>Top 10 Nifty 500 Screener Picks</b>\n\n" +
            "\n".join(formatted_lines)
        )
        
        with st.spinner("Broadcasting to Telegram..."):
            res = send_telegram(message)
            if res.get("ok"):
                st.success("Top 10 successfully sent to Telegram!")
            else:
                st.error(f"Error: {res.get('description')}")
