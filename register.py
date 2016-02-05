from bs4 import BeautifulSoup


class Register:

    def parse_link(self, content):
        soup = BeautifulSoup(content)
        name = soup.find("div", {"class": "article_head"})
        if name:
            name = name.find("h1")
        if name:
            name = name.getText()
        else:
            name = ''

        paragraphs = soup.select('div.body p')
        text = name + '\n'
        for p in paragraphs:
            text += p.get_text()
            text += '\n'
        return text

    def parse_page(self, content):
        soup = BeautifulSoup(content)
        links = soup.select('a.story_link')
        return [link['href'] for link in links if "www.theregister.co.uk"
                in link['href']]

    def __init__(self, section):
        self.name = 'Register'
        self.__basepage = 'http://www.theregister.co.uk/'
        self.main_page = self.__basepage + section
        self.encoding = 'UTF8'
        self.lang = "english"
