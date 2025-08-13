from entity.headlines.portal import Portal


class Valor(Portal):
    def __init__(self):
        self.name = 'VALOR'
        self.url = 'https://valor.globo.com/'
        self.soup_function = 'soup.find("a", {"class": "bstn-dedupe-url"}).text'
        super()
        self.save_head_line()