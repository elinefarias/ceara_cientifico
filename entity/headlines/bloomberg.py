import urllib3
from bs4 import BeautifulSoup
import requests

http = urllib3.PoolManager()


class Bloomberg():
    def __init__(self):
        self.name = 'BLOOMBERG'
        self.url = 'https://www.bloomberg.com/politics'
        self.head_line = None
        self.link = None
        self.pipeline()

    def pipeline(self):
        self.get_head_line_and_link()
        print(self.head_line)
        print(self.link)

    def get_head_line_and_link(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.result = soup.find("div", {"class": "styles_storyContainer__JKW0t"})
        soup = self.result
        news = soup.find_all("a")
        first_news = news[0]
        self.link = f'https://www.bloomberg.com/{first_news.get("href")}'
        self.head_line = soup.get_text().strip()
