import datetime as dt
import os
from newsapi import NewsApiClient
from dotenv import load_dotenv
import json

COMPANY_NAMES = ["Tesla Inc", "Bitcoin"]


class News:

    def __init__(self, topic=None):
        """
        Class that handles the mining of news for target company(s).
        topic: The target company to mine news for, str or lst of str.
        """
        if topic is None:
            self.topic = COMPANY_NAMES
        else:
            if len([topic]) == 1:
                self.topic = [topic]
            else:
                self.topic = topic

        today = dt.date.today()
        yesterday = today - dt.timedelta(days=2)
        self.today = today.strftime("%Y-%m-%d")
        self.day_before = yesterday.strftime("%Y-%m-%d")

        load_dotenv("C:/env/.env.txt")
        self.apikey = os.getenv("api_key_news")

        self.api = NewsApiClient(self.apikey)
        self.news = {}
        self.top_results()

    def top_results(self, amount=3):
        """Returns top [amount] news articles related to topic"""

        for topic in self.topic:
            response = self.api.get_everything(q=topic, language='en', sort_by='relevancy',
                                               from_param=self.day_before, to=self.today)

            self.news[topic] = response['articles'][0:amount]

            with open(f"{topic}.json", "w") as f:
                json.dump(response, f)

    def get_info(self):
        output = {}
        for topic in self.news:
            for key in self.news[topic]:
                output[key['title']] = key['description']
        return output

