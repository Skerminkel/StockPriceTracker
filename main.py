import os
from dotenv import load_dotenv as lenv
from twilio.rest import Client
from stock_class import Stock
from news_class import News
from twilio.http.http_client import TwilioHttpClient

stock_dict = {
    "GOOGL": "Google",
    "TSLA": "Tesla"
}


def create_message(stock_in, news_in, name_in):

    change = stock_in.change()
    symbol = "🔺" if change > 0 else "🔻"
    message = f"{symbol} {name_in}: {round(change, 1)}\n"

    if change is not None:
        raw_data = news_in.get_info()

        for topic in raw_data:

            title = f"Title: {topic}"
            brief = f"Brief: {raw_data[topic]}"
            body = f"\n{title}\n{brief}\n"
            message += body

        return f"{message}"


# proxy_client = TwilioHttpClient()
# proxy_client.session.proxies = {'https': os.environ['https_proxy']}

lenv("C:/env/.env.txt")
account_sid = os.getenv("account_sid")

auth_token = os.getenv("auth_token")
client = Client(account_sid, auth_token)

# client = Client(account_sid, auth_token, http_client=proxy_client)

for code in stock_dict:

    stock = Stock(code)
    name = stock_dict[code]
    news = News(name)

    message = client.messages.create(
        body=create_message(stock, news, name), from_='+13865165795',
        to='+27711472103')


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
