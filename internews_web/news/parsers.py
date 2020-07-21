import requests
from bs4 import BeautifulSoup
from .locators import BaseLocator


class BaseStaticParser:

    def __init__(self, locator: BaseLocator):
        self.locator = locator

    def get_articles_data(self) -> list:
        result = []
        parsed_articles = self.get_news()
        for article in parsed_articles:
            result.append((self.locator.get_link(article), self.locator.get_headline(article)))
        return result

    def get_page_html(self) -> str:
        return requests.get(self.locator.get_full_news_path()).text

    def get_news(self):
        return self.soup().select(self.locator.NEWS_SELECTOR)

    def soup(self):
        return BeautifulSoup(self.get_page_html(), 'html.parser')
