import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import locators


class BaseParser(ABC):
    @abstractmethod
    def get_locators(self):
        pass

    def get_result(self):
        result = []
        for article in self.get_news(self.get_locators().BASE_URL, self.get_locators().NEWS_SELECTOR):
            headline_name_link = []
            headline_name_link.append(self.get_locators().get_headline(article))
            headline_name_link.append(self.get_locators().get_link(article))
            result.append(headline_name_link)
        return result

    def get_news(self, url, css_selector):
        return self.soup(url).select(css_selector)

    def get_page_html(self, url: str):
        return requests.get(url)

    def soup(self, url):
        return BeautifulSoup(self.get_page_html(url).text, 'html.parser')


class RiaParser(BaseParser):
    def get_locators(self):
        return locators.RiaLocators()














