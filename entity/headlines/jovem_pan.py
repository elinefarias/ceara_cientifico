from entity.headlines.portal import Portal


class JovemPan(Portal):
    def __init__(self):
        self.name = 'JOVEM PAN'
        self.url = 'https://jovempan.com.br/'
        self.soup_function = 'soup.find("h2", {"class": "title"}).text'
        super()
        self.save_head_line()