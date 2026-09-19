import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="TradingView Telegram Dashboard", page_icon="📈", layout="centered")

st.title("📈 TradingView Telegram Alert Dashboard")
st.markdown("Manage your Telegram bot integration and monitor incoming screener alerts.")

# Sidebar Configuration
st.sidebar.header("Telegram Settings")
bot_token = st.sidebar.text_input("Bot Token", type="password", value=os.getenv("TELEGRAM_BOT_TOKEN", ""))
chat_id = st.sidebar.text_input("Chat ID", value=os.getenv("TELEGRAM_CHAT_ID", ""))

def send_telegram(message):
    if not bot_token or not chat_id:
        return {"ok": False, "description": "Bot Token or Chat ID is missing."}
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(url, json=payload)
    return response.json()

# Tabs for Organization
tab1, tab2, tab3 = st.tabs(["🚀 Test Alert", "📋 Webhook Logs", "⚙️ Deployment Guide"])

with tab1:
    st.subheader("Send a Test Notification")
    test_msg = st.text_area(
        "Message Body (HTML supported)", 
        "🚨 <b>NIFTY Screener Test</b>\n\n📈 <b>Stock:</b> RELIANCE\n💵 <b>Price:</b> ₹2,950.00\n📊 <b>Volume:</b> 1.5M"
    )
    if st.button("Send Test Message to Telegram"):
        with st.spinner("Sending..."):
            result = send_telegram(test_msg)
            if result.get("ok"):
                st.success("Message sent successfully to Telegram!")
            else:
                st.error(f"Failed to send: {result.get('description', 'Unknown error')}")

with tab2:
    st.subheader("Recent Webhook Logs")
    log_file = "webhook_logs.json"
    
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                logs = json.load(f)
            if logs:
                for log in reversed(logs[-10:]):  # Show last 10 entries
                    st.json(log)
            else:
                st.info("No webhook alerts recorded yet.")
        except Exception as e:
            st.error(f"Error reading log file: {e}")
    else:
        st.info("Log file not found yet. Webhooks will appear here once received.")
        if st.button("Generate Sample Log"):
            sample_logs = [{"ticker": "TCS", "close": "4120.50", "volume": "850K", "time": "2026-06-06"}]
            with open(log_file, "w") as f:
                json.dump(sample_logs, f)
            st.rerun()

with tab3:
    st.subheader("Architecture Note")
    st.markdown("""
    Streamlit runs interactive UI apps and cannot natively accept raw HTTP POST webhooks directly without a backing endpoint. 
    
    **Recommended Setup:**
    1. Deploy a lightweight receiver (like Flask/FastAPI) to handle incoming TradingView webhooks and save them to `webhook_logs.json`.
    2. Deploy this Streamlit app on **Streamlit Community Cloud** pointing to the same log storage or database to view your live feed and test your bot configuration on the go.
    """)
