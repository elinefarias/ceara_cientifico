import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()


class NbcNews():
    def __init__(self):
        self.name = 'NBC NEWS'
        self.url = 'https://www.nbcnews.com/'
        self.head_line = None
        self.link = None
        self.pipeline()

    def pipeline(self):
        self.get_head_line_and_link()
        print(self.head_line)
        print(self.link)

    def get_head_line_and_link(self):
        page = http.request('GET', self.url)
        soup = BeautifulSoup(page.data, 'html.parser')
        self.result = soup.find("div", {"class": "container-side__text-content no-dek no-author-timestamp"})
        soup = self.result
        news = soup.find_all("a")
        first_news = news[0]
        self.link = first_news.get("href")
        self.head_line = soup.get_text().strip()
