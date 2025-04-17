import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
import requests
import os
import time


load_dotenv()

# --- Configuration ---
TICKER = "AAPL"
SHORT_MA = 20
LONG_MA = 50
TIMEFRAME = "1h"  # Use "1d" for daily
WEBHOOK_URL = os.getenv("medium_term_webhook")
CHECK_INTERVAL_SECONDS = 3600  # Run every hour

# --- Discord Send Function ---
def send_to_discord(message: str):
    if not WEBHOOK_URL:
        print("Webhook URL not found in environment variables.")
        return

    payload = {"content": message}
    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        print("✅ Message sent successfully.")
    else:
        print(f"❌ Failed to send message: {response.status_code}")

# --- Fetch Data from Yahoo Finance ---
def fetch_data(ticker, period="60d", interval="1h"):
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
    df.dropna(inplace=True)
    return df

# --- Generate Buy/Sell Signals ---
def generate_signal(df):
    df["SMA_short"] = df["Close"].rolling(window=SHORT_MA).mean()
    df["SMA_long"] = df["Close"].rolling(window=LONG_MA).mean()
    df["Signal"] = 0
    df.iloc[SHORT_MA:, df.columns.get_loc("Signal")] = (
        (df["SMA_short"][SHORT_MA:] > df["SMA_long"][SHORT_MA:]).astype(int)
    )
    df["Position"] = df["Signal"].diff()
    return df

# --- Check for the Latest Signal ---
def check_for_latest_signal(df):
    latest_row = df.iloc[-1]
    try:
        position = latest_row["Position"].item() if hasattr(latest_row["Position"], 'item') else latest_row["Position"]
    except ValueError:
        position = None

    if position == 1:
        return f"📈 BUY signal for {TICKER} at ${latest_row['Close']:.2f}"
    elif position == -1:
        return f"📉 SELL signal for {TICKER} at ${latest_row['Close']:.2f}"
    return None

# --- Run the Trading Bot ---
def run_trading_bot():
    print("⏳ Checking for trading signals...")
    df = fetch_data(TICKER, interval=TIMEFRAME)
    df = generate_signal(df)
    signal_msg = check_for_latest_signal(df)
    if signal_msg:
        send_to_discord(signal_msg)
    else:
        print("📭 No signal at this time.")

# --- Main Loop ---
if __name__ == "__main__":
    while True:
        run_trading_bot()
        print(f"🔁 Sleeping for {CHECK_INTERVAL_SECONDS // 60} minutes...\n")
        time.sleep(CHECK_INTERVAL_SECONDS)
