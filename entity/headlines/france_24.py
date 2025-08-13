from entity.headlines.portal import Portal



class France24(Portal):
    def __init__(self):
        self.name = 'FRANCE 24'
        self.url = 'https://www.france24.com/fr/'
        self.soup_function = 'soup.find("div", {"class": "article__title"}).text'
        super()
        self.save_head_line()
