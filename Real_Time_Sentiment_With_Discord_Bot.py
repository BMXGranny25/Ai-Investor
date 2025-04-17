import os
import requests
from textblob import TextBlob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEBHOOK_URL = os.getenv("main_webhook_url")

# Stocks to monitor
stocks_to_track = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NFLX', 'META', 'NVDA', 'WELL', 'AMD', 'TEM', 'SHOP', 'ASML', 'F','SPY', 'QQQ', 'DIA', 'ARKK',
    'BRK.B', 'JPM', 'JNJ', 'XOM', 'PG',
    'V', 'MA', 'UNH', 'HD', 'PEP',
    'INTC', 'QCOM', 'AVGO', 'ADBE', 'CRM',
    'WMT', 'COST', 'TGT', 'MCD', 'NKE',
    'SBUX', 'BA', 'CAT', 'GE', 'GM',
    'PFE', 'MRK', 'LLY', 'ABBV', 'DIS',
    'VZ', 'T']



# Fetch news sentiment
def get_news_sentiment(stock):
    url = f"https://newsapi.org/v2/everything?q={stock}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    print(f"Fetching news for {stock}...")
    response = requests.get(url).json()

    if 'articles' not in response:
        print(f"No articles found for {stock}")
        return 0

    headlines = [article.get("title", "") for article in response["articles"][:10] if article.get("title")]

    if not headlines:
        print(f"No valid headlines for {stock}")
        return 0

    sentiments = [TextBlob(headline).sentiment.polarity for headline in headlines]
    score = sum(sentiments) / len(sentiments) if sentiments else 0
    print(f"Sentiment for {stock}: {score:.2f}")
    return score

# Check all stocks and build sentiment log
def check_stocks():
    sentiment_log = ""

    for stock in stocks_to_track:
        score = get_news_sentiment(stock)
        # Buy/Sell Signal
        if score > 0.4:
            print(f"🚀 BUY Alert: {stock} | Sentiment Score: {score:.2f}")
            buy_or_sell = '🚀 BUY Alert:'
        elif score < -0.4:
            print(f"⚠️ SELL Alert: {stock} | Sentiment Score: {score:.2f}")
            buy_or_sell = '⚠️ SELL Alert:'
        else:
            print(f"✅ Neutral: {stock} | Sentiment Score: {score:.2f}")
            buy_or_sell = '✅ Neutral:'
        sentiment_log += f"{buy_or_sell} {stock}: {score:.2f}\n"

    return sentiment_log.strip()

# Send summary via webhook
def send_sentiment_summary(messages):
    if not WEBHOOK_URL:
        print("Webhook URL not set in .env file.")
        return

    data = {
        "content": f"@everyone 📊 Sentiment Summary\n```\n{messages}\n```"
    }

    response = requests.post(WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("✅ Message sent successfully!")
    else:
        print(f"❌ Failed to send message: {response.status_code} | {response.text}")

# Run the full process
if __name__ == "__main__":
    summary = check_stocks()
    send_sentiment_summary(summary)


"""
The sentiment score in this script is generated using **TextBlob**, which is a simple library for processing textual data. Specifically, it uses **polarity** to quantify sentiment based on text input. Here's a breakdown of how it works:

### **Sentiment Score (Polarity)**

1. **TextBlob's Polarity**:
   - **Polarity** is a number that ranges from **-1.0 to 1.0**.
     - **1.0** indicates a **positive** sentiment.
     - **-1.0** indicates a **negative** sentiment.
     - **0** indicates **neutral** sentiment.

2. **Sentiment Calculation in Your Script**:
   - For each stock, you gather **news headlines** from the News API.
   - TextBlob is applied to each headline to calculate the **sentiment polarity** for each.
   - The average of the sentiment scores of all the headlines is then computed for that stock.

### **Steps to Calculate Sentiment**:
1. **Fetch News Headlines**:
   You fetch the latest news articles for a given stock (e.g., `AAPL`, `MSFT`, etc.) using the **News API**.

2. **Sentiment Analysis on Headlines**:
   Each headline fetched is processed by **TextBlob**:
   ```python
   sentiment_score = TextBlob(headline).sentiment.polarity
   ```
   - **TextBlob** returns a sentiment polarity score for each headline.
   
3. **Averaging the Sentiment**:
   After processing each headline, you calculate the **average** of the sentiment scores for the top 10 headlines:
   ```python
   score = sum(sentiments) / len(sentiments) if sentiments else 0
   ```
   If there are no valid headlines or sentiment scores, it returns a neutral score of `0`.

### **Types of Sentiment**:
- **Positive Sentiment**: Headline text like "Apple's new product is revolutionary!" might yield a polarity close to **1.0**.
- **Negative Sentiment**: A headline like "Apple faces lawsuits over faulty product" could yield a polarity near **-1.0**.
- **Neutral Sentiment**: A headline like "Apple announces new iPhone specs" might give a polarity closer to **0.0**.

### **Interpretation**:
- **> 0.4** → Positive sentiment, often triggering a "BUY" alert.
- **< -0.4** → Negative sentiment, often triggering a "SELL" alert.
- **Between -0.4 and 0.4** → Neutral sentiment.

---

### Example of the Score Calculation:

- **Headline 1**: "Apple stocks rise after new iPhone announcement" → Sentiment = **0.3** (positive)
- **Headline 2**: "Apple's earnings fall due to weaker iPhone sales" → Sentiment = **-0.2** (negative)
- **Headline 3**: "Apple announces new quarterly dividend" → Sentiment = **0.1** (positive)

Average Sentiment for **AAPL**:
```python
(0.3 + (-0.2) + 0.1) / 3 = 0.0667 (Neutral)
```

### **TextBlob Sentiment Calculation**:
- **TextBlob** uses a lexicon of predefined positive and negative words.
- It calculates the **polarity** of each word in the sentence and aggregates those values to form an overall sentiment score for the entire sentence.
- This score is then averaged for all the headlines to give you a general sentiment for the stock.

"""