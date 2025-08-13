from entity.headlines.portal import Portal


class CnnBrasil(Portal):
    def __init__(self):
        self.name = 'CNN BRASIL'
        self.url = 'https://www.cnnbrasil.com.br/'
        self.soup_function = 'soup.find("h2", {"class": "block__news__title"}).text'
        super()
        self.save_head_line()