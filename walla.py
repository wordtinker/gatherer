from bs4 import BeautifulSoup


class Walla:

    def parse_link(self, content):
        soup = BeautifulSoup(content)
        name = soup.find("article").find("h1")
        if name:
            name = name.get_text()
        else:
            name = ''
        header = soup.find("article").find("h2")
        if  header:
            header = header.get_text()
        else:
            header = ''
        paragraphs = soup.select("article section.article-content p")
        text = name + '\n'+ header + '\n'
        for p in paragraphs:
            text += p.get_text()
            text += '\n'
        return text

    def parse_page(self, content):
        soup = BeautifulSoup(content)
        links = soup.select('article a')
        return [self.__basepage + link['href'] for link in links]

    def __init__(self, section):
        self.name = 'Walla'
        self.__basepage = 'http://news.walla.co.il'
        self.main_page = self.__basepage + section
        self.encoding = 'UTF8'
        self.lang = "hebrew"
