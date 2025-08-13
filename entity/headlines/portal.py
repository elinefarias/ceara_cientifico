import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()


class Portal():
    def __init__(self, name, url, soup_function):
        self.name = name
        self.url = url
        self.soup_function = soup_function
        self.summary = None

    def get_head_line(self):
        page = http.request('GET', self.url)
        soup = BeautifulSoup(page.data, 'html.parser')
        self.result = eval(self.soup_function)
    
    def save_head_line(self):
        self.get_head_line()
        self.summary = f"{self.name}: {self.result.strip()}."
    