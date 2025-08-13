from entity.headlines.portal import Portal


class Uol(Portal):
    def __init__(self):
        self.name = 'UOL'
        self.url = 'https://www.uol.com.br'
        self.soup_function = 'soup.find("h3", {"class": "title__element"}).text'
        super()
        self.save_head_line()