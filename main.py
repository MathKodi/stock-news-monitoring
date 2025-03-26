import requests
from datetime import datetime, timedelta
from twilio.rest import Client

import config

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
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


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
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

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

