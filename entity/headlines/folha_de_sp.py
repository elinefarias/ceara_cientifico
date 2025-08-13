from entity.headlines.portal import Portal



class FolhaDeSp(Portal):
    def __init__(self):
        self.name = 'FOLHA DE SP'
        self.url = 'https://www.folha.uol.com.br/'
        self.soup_function = 'soup.find("h2", {"class": "c-main-headline__title"}).text'
        super()
        self.save_head_line()