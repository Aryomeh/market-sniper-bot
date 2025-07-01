# 📈 MarketPulse Bot

A Telegram bot that delivers real-time cryptocurrency and stock market updates to your channel.

![Bot Demo](https://img.shields.io/badge/status-active-brightgreen) 
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Render](https://img.shields.io/badge/deployed%20on-render-5f45bb)

## ✨ Features
- Hourly price updates for:
  - **Crypto**: BTC, ETH, SOL
  - **Stocks**: AAPL, TSLA, AMZN
- Automated news alerts
- Multi-channel support
- 24/7 uptime via Render

## 🚀 Deployment

### Prerequisites
- Python 3.10+
- Telegram Bot Token ([@BotFather](https://t.me/BotFather))
- Finnhub API Key (free tier)

### 1. Render Setup (1-Click)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yourusername/market-sniper-bot)

### 2. Manual Setup
```bash
# Clone repo
git clone https://github.com/yourusername/market-sniper-bot.git
cd market-sniper-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
echo "TELEGRAM_TOKEN=your_token_here" > .env
echo "FINNHUB_KEY=your_key_here" >> .env

# Run bot
python main.py
