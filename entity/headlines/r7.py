from entity.headlines.portal import Portal


class R7(Portal):
    def __init__(self):
        self.name = 'R7'
        self.url = 'https://www.r7.com/'
        self.soup_function = 'soup.find("a", {"class": "r7-flex-title-h3__link"}).text'
        super()
        try:
            self.save_head_line()
        except:
            self.soup_function = 'soup.find("a", {"class": "r7-flex-title-h1__link"}).text'
            self.save_head_line()