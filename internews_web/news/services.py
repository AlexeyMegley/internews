import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class AbstractParser(ABC):
    @abstractmethod
    def get_news(self, url: str, css_selector: str):
        pass

    def get_page_html(self, url: str):
        return requests.get(url)

    def soup(self, url):
        return BeautifulSoup(self.get_page_html(url).text, 'html.parser')


class RussiaTodayParser(AbstractParser):
    def get_news(self, url, css_selector):
        articles = self.soup(url).select(css_selector)
        result = []
        for article in articles:
            head_linkhead = []
            head_linkhead.append(article.string)
            head_linkhead.append(article.get('href'))
            result.append(head_linkhead)
        return result
