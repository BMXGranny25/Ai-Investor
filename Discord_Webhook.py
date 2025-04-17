import requests
import os
from dotenv import load_dotenv

load_dotenv()
def send_updates(messages):
    load_dotenv()
    webhook_url = os.getenv("main_webhook_url")
    message = {
        "content": messages
    }

    response = requests.post(webhook_url, json=message)

    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}")

#message="Sentiment for AAPL: -0.07 ✅ Neutral: AAPL | Sentiment Score: -0.07\nFetching news for MSFT...\nSentiment for MSFT: 0.10\n✅ Neutral: MSFT | Sentiment Score: 0.10\nFetching news for GOOGL...\nSentiment for GOOGL: 0.03\n✅ Neutral: GOOGL | Sentiment Score: 0.03\nFetching news for TSLA...\nSentiment for TSLA: 0.11\n✅ Neutral: TSLA | Sentiment Score: 0.11\nFetching news for AMZN...\nSentiment for AMZN: 0.01\n✅ Neutral: AMZN | Sentiment Score: 0.01\nFetching news for NFLX...\nSentiment for NFLX: 0.06\n✅ Neutral: NFLX | Sentiment Score: 0.06\nFetching news for META...\nSentiment for META: 0.00\n✅ Neutral: META | Sentiment Score: 0.00\nFetching news for NVDA...\nSentiment for NVDA: 0.00\n✅ Neutral: NVDA | Sentiment Score: 0.00\nFetching news for WELL...\nSentiment for WELL: 0.17\n✅ Neutral: WELL | Sentiment Score: 0.17\nFetching news for AMD...\nSentiment for AMD: 0.03\n✅ Neutral: AMD | Sentiment Score: 0.03\nFetching news for TEM...\nSentiment for TEM: -0.11\n✅ Neutral: TEM | Sentiment Score: -0.11\nFetching news for SHOP...\nSentiment for SHOP: 0.01\n✅ Neutral: SHOP | Sentiment Score: 0.01\nFetching news for ASML...\nSentiment for ASML: -0.01\n✅ Neutral: ASML | Sentiment Score: -0.01\nFetching news for F...\nSentiment for F: 0.08\n✅ Neutral: F | Sentiment Score: 0.08"

def Send_Youtube_Summary(messages):
    load_dotenv()
    webhook_url = os.getenv("main_webhook_url")
    message = {
        "content": messages
    }

    response = requests.post(webhook_url, json=message)

    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}")
#send_updates('@everyone 🚀📈 \n' + message)