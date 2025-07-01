import requests
import yfinance as yf
import time
from telegram import Bot
from flask import Flask
from threading import Thread
import os

# === START: Keep Alive Web Server ===
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# ✅ SECURE BOT TOKEN from Render Environment Variable
BOT_TOKEN = os.getenv("7501305311:AAFm3h66QwupjNca2TdLYKwUkK-c4VoacWQ")  # Token must be stored in Render
CHANNEL_ID = "-1002832342598"       # This is safe

bot = Bot(7501305311:AAFm3h66QwupjNca2TdLYKwUkK-c4VoacWQ)

def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin&vs_currencies=usd"
    data = requests.get(url).json()
    return {
        "BTC": data["bitcoin"]["usd"],
        "ETH": data["ethereum"]["usd"],
        "SOL": data["solana"]["usd"],
        "BNB": data["binancecoin"]["usd"]
    }

def get_stock_prices():
    tickers = ["AAPL", "GOOGL", "TSLA", "^DJI", "^GSPC"]
    data = yf.download(tickers, period="1d", interval="1m")
    latest = data["Close"].iloc[-1]
    return {
        "Apple (AAPL)": round(latest["AAPL"], 2),
        "Google (GOOGL)": round(latest["GOOGL"], 2),
        "Tesla (TSLA)": round(latest["TSLA"], 2),
        "Dow Jones (DJI)": round(latest["^DJI"], 2),
        "S&P 500 (GSPC)": round(latest["^GSPC"], 2),
    }

def format_message(crypto, stocks):
    msg = "📊 *Market Update*\n\n"
    msg += "🪙 *Crypto Prices:*\n"
    for coin, price in crypto.items():
        msg += f"{coin}: ${price:,}\n"
    msg += "\n💼 *Stock Market:*\n"
    for stock, price in stocks.items():
        msg += f"{stock}: ${price:,}\n"
    return msg

# === KEEP ALIVE + MAIN LOOP ===
keep_alive()

while True:
    try:
        crypto = get_crypto_prices()
        stocks = get_stock_prices()
        message = format_message(crypto, stocks)
        bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
        print("✅ Sent market update at", time.ctime())
       time.sleep(10800)  # 3 hours
    except Exception as e:
        print("❌ Error:", e)
        time.sleep(600)  # Retry after 10 minutes
