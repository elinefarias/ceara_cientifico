from entity.headlines.portal import Portal


class Infomoney(Portal):
    def __init__(self):
        self.name = 'INFOMONEY'
        self.url = 'https://www.infomoney.com.br/'
        self.soup_function = 'soup.find("a", {"class": "cover-link"})["title"]'
        super()
        self.save_head_line()