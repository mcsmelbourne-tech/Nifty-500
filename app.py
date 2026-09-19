import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Credentials (Set these as environment variables on your server)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    
    # Extract details from TradingView alert payload
    ticker = data.get("ticker", "N/A")
    close_price = data.get("close", "N/A")
    volume = data.get("volume", "N/A")
    time_stamp = data.get("time", "N/A")
    condition = data.get("condition", "Screener Match")

    # Format Telegram message
    message = (
        f"🚨 <b>NIFTY Screener Alert</b>\n\n"
        f"📈 <b>Stock:</b> {ticker}\n"
        f"💵 <b>Price:</b> ₹{close_price}\n"
        f"📊 <b>Volume:</b> {volume}\n"
        f"🔍 <b>Condition:</b> {condition}\n"
        f"⏰ <b>Time:</b> {time_stamp}"
    )

    send_telegram_message(message)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
