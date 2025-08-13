from entity.headlines.portal import Portal



class DiarioDoNordeste(Portal):
    def __init__(self):
        self.name = 'DIÁRIO DO NORDESTE'
        self.url = 'https://diariodonordeste.verdesmares.com.br/'
        self.soup_function = 'soup.find("h2", {"class": "m-c-teaser__heading"}).text'
        super()
        self.save_head_line()