#!/usr/bin/env python3
# ====== IMPORTS ======
import os
import requests
import asyncio
from threading import Thread
from flask import Flask
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pytz import utc
import nest_asyncio

# ====== CONFIGURATION ======
# Get environment variables (set these in Render dashboard)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
finnhub_key = os.environ.get('FINNHUB_KEY')

# ====== FLASK KEEP-ALIVE ======
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ MarketPulse Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)  # Render's default port

# ====== PRICE FETCHER ======
def fetch_prices():
    try:
        cg = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd").json()
        stocks = {
            'AAPL': requests.get(f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={finnhub_key}").json(),
            'TSLA': requests.get(f"https://finnhub.io/api/v1/quote?symbol=TSLA&token={finnhub_key}").json(),
            'AMZN': requests.get(f"https://finnhub.io/api/v1/quote?symbol=AMZN&token={finnhub_key}").json()
        }
        
        return (
            f"📈 *Market Update*\n\n"
            f"🪙 *Crypto*\n"
            f"• BTC: ${cg['bitcoin']['usd']}\n"
            f"• ETH: ${cg['ethereum']['usd']}\n"
            f"• SOL: ${cg['solana']['usd']}\n\n"
            f"📊 *Stocks*\n"
            f"• AAPL: ${stocks['AAPL']['c']}\n"
            f"• TSLA: ${stocks['TSLA']['c']}\n"
            f"• AMZN: ${stocks['AMZN']['c']}"
        )
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ====== BOT FUNCTIONS ======
async def send_prices(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=fetch_prices(),
        parse_mode='Markdown'
    )

async def track_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    print(f"New chat: {chat.title or 'Private'} (ID: {chat.id})")

# ====== MAIN SETUP ======
async def main():
    # Initialize
    nest_asyncio.apply()
    bot_app = Application.builder().token(TOKEN).build()
    
    # Handlers
    bot_app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_chat))
    
    # Scheduler
    scheduler = AsyncIOScheduler(timezone=utc)
    scheduler.add_job(
        send_prices,
        IntervalTrigger(hours=3),  # Every 3 hours
        id="price_updates"
    )
    scheduler.start()
    
    # Start Flask in background
    Thread(target=run_flask).start()
    
    # Run bot
    await bot_app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
