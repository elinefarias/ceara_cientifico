import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()

class UsaToday():
    def __init__(self):
        self.name = 'USA TODAY'
        self.url = 'https://www.usatoday.com/'
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
        self.result = soup.find_all("div", class_="gnt_m_tt_col")
        soup = self.result[1]
        news = soup.find_all("a")
        first_news = news[0]
        self.link = f'{self.url}{first_news.get("href")}'
        self.head_line = first_news.get_text().strip()

