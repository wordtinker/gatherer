from bs4 import BeautifulSoup


class Guardian:

    def parse_link(self, content):
        soup = BeautifulSoup(content)
        # name = soup.select("div#main-article-info")
        name = soup.select('div.content__standfirst')
        if len(name) > 0:
            name = name[0].get_text()
        else:
            name = ''
        # paragraphs = soup.select("div#article-body-blocks p")
        paragraphs = soup.select('div.content__article-body p')
        text = name + '\n'
        for p in paragraphs:
            text += p.get_text()
            text += '\n'
        return text

    def parse_page(self, content):
        soup = BeautifulSoup(content)
        # links = soup.select('div#latestnewsukpick a.link-text')
        links = soup.select('a.fc-item__link')
        return [link['href'] for link in links]

    def __init__(self, section):
        self.name = 'Guardian'
        self.__basepage = 'http://www.theguardian.com'
        self.main_page = self.__basepage + section
        self.encoding = 'UTF8'
        self.lang = "english"
