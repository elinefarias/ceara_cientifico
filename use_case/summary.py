import config
from entity.headlines.the_new_york_times import TheNewYorkTimes
from entity.headlines.the_washington_post import TheWashigtonPost
from entity.headlines.usa_today import UsaToday
from entity.headlines.fox_news import FoxNews
from entity.headlines.nbc_news import NbcNews
from entity.headlines.bloomberg import Bloomberg
from entity.headlines.news_week import NewsWeek
from entity.headlines.bbc import Bbc
from langchain_openai import ChatOpenAI
import urllib3
from bs4 import BeautifulSoup
import requests

http = urllib3.PoolManager()


def summary():
    links = get_links()
    summaries = []
    sentiments = []
    for i in links:
        news = read_news(i)
        response = entity_search(news, 'Biden')
        if response == 'YES':
            sentiments.append(check_sentiment(news, 'Biden'))
            summary = summarize(news, 'Biden')
            summaries.append(summary)
    texts = ''.join(summaries)
    if len(sentiments) > 0:
        sentiment = max(set(sentiments), key = sentiments.count)
    else:
        sentiment = 'No sentiments today'
    return f"""Sentiment: \n\n {sentiment}. \n\n
    Summary: \n\n {summarize_all(texts, 'Biden')}"""


def get_links():
    portal_dict = {
        #'bbc': {'instance': Bbc()},
        'news_week': {'instance': NewsWeek()},
        #'bloomberg': {'instance': Bloomberg()},
        'nbc_news': {'instance': NbcNews()},
        'fox_news': {'instance': FoxNews()},
        'usa_today': {'instance': UsaToday()},
        'the_washington_post': {'instance': TheWashigtonPost()},
        'the_new_york_times': {'instance': TheNewYorkTimes()}
    }

    links = []

    for key, value in portal_dict.items():
        politic_check = check_subject(portal_dict[key]['instance'].head_line)
        if politic_check == 'YES':
            links.append(portal_dict[key]['instance'].link)

    return links


def check_subject(headline):
    llm = ChatOpenAI(api_key=config.OPENAI_API_KEY)
    response = llm.invoke(f'Answer YES or NO if this content: {headline} is related to politics. If there is ambiguity, choose YES. Example: Population growth breaks record.Answer: NO. Example: High temperatures due to global warming. Answer: NO')
    return response.content


def read_news(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.get_text()


def entity_search(name, text):
    llm = ChatOpenAI(api_key=config.OPENAI_API_KEY)
    response = llm.invoke(f'Answer YES or NO if this name is explicitly mentioned in this text: NAME: {name}. TEXT: {text}.')
    return response.content


def check_sentiment(text, name):
    llm = ChatOpenAI(api_key=config.OPENAI_API_KEY)
    response = llm.invoke(f'Return the Sentiment Analysis (POSITIVE, NEUTRAL or NEGATIVE) regarding {name} in this text: {text}. Return only the sentiment, do not write anything else.')
    return response.content


def summarize(text, name):
    llm = ChatOpenAI(api_key=config.OPENAI_API_KEY)
    response = llm.invoke(f'Make a short summary of this text, focusing on the excerpt in which {name} is mentioned: TEXT: {text}')
    return response.content


def summarize_all(texts, name):
    if len(texts) > 0:
        llm = ChatOpenAI(api_key=config.OPENAI_API_KEY)
        response = llm.invoke(f'Make a discursive text joining all these texts, focusing on the excerpt in which {name} is mentioned. TEXTS: {texts}.')
        return response.content
    else:
        return f'No mentions of {name} today'
