import requests
from datetime import datetime, timedelta
from twilio.rest import Client

import config

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

from datetime import datetime, timedelta

today = datetime.today()
yesterday = today - timedelta(days=1)
beforeyesterday = today - timedelta(days=2)

if yesterday.weekday() >= 5:
    days_to_subtract = 2 if yesterday.weekday() == 5 else 3
    yesterday = today - timedelta(days=days_to_subtract)

beforeyesterday = yesterday - timedelta(days=1)

if beforeyesterday.weekday() >= 5:
    days_to_subtract = 2 if beforeyesterday.weekday() == 5 else 3
    beforeyesterday = yesterday - timedelta(days=days_to_subtract)


data_yesterday = yesterday.strftime("%Y-%m-%d")
data_beforeyesterday = beforeyesterday.strftime("%Y-%m-%d")

print(data_yesterday)
print(data_beforeyesterday)

api_key_alphavantage = config.alphavantage_api_key
data = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={api_key_alphavantage}")
stock_price = data.json()["Time Series (Daily)"]
yesterday_price = float(stock_price[data_yesterday]["4. close"])
before_yesterday_price = float(stock_price[data_beforeyesterday]["4. close"])
print(yesterday_price)
print(before_yesterday_price)

api_key_news = config.news_api_key
account_sid = config.account_sid
auth_token = config.auth_token
phone = config.myphone
twiliophone = config.twiliophone

def check_percentage_change(yesterday, before_yesterday):
    client = Client(account_sid, auth_token)
    change = ((yesterday - before_yesterday) / before_yesterday) * 100
    if abs(change) >= 5:
        data_news = requests.get(f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={data_yesterday}&sortBy=popularity&apiKey={api_key_news}")
        for _ in range(3):
            if change > 0:
                message = client.messages.create(body=f"TSLA: 🔺{round(abs(change))}%Headline: {data_news.json()["articles"][_]["title"]}", from_=twiliophone ,to=phone)
                print(message.sid)
            else:
                message = client.messages.create(
                    body=f"TSLA: 🔻{round(abs(change))}%Headline: {data_news.json()["articles"][_]["title"]}",
                    to=phone,
                    from_=twiliophone)
                print(message.sid)

check_percentage_change(yesterday=yesterday_price, before_yesterday=before_yesterday_price)


