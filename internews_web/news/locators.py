from abc import ABC, abstractmethod
from urllib.parse import urljoin


class BaseLocators(ABC):
    BASE_URL = ' '
    NEWS_URL_PATH = ' '
    NEWS_SELECTOR = ' '

    @classmethod
    def get_full_news_path(cls):
        return urljoin(cls.BASE_URL, cls.NEWS_URL_PATH)

    @abstractmethod
    def get_link(self, article):
        pass

    @abstractmethod
    def get_headline(self, article):
        pass


class RussiaTodayLocators(BaseLocators):
    BASE_URL = 'https://russian.rt.com/'
    NEWS_SELECTOR = 'div.card__heading.card__heading_main-news a'

    def get_link(self, article):
        return article.get('href')

    def get_headline(self, article):
        return article.string


class RiaLocators(BaseLocators):
    BASE_URL = 'https://ria.ru/'
    NEWS_SELECTOR = 'span.elem-info__share .share'

    def get_link(self, article):
        return article.get('data-url')

    def get_headline(self, article):
        return article.get('data-title')


class RainLocators(BaseLocators):
    BASE_URL = 'https://tvrain.ru/news/'
    NEWS_SELECTOR = 'h3 a'

    def get_link(self, article):
        return article.get('href')

    def get_headline(self, article):
        return article.string


class FoxNewsLocators(BaseLocators):
    BASE_URL = 'https://www.foxnews.com/'
    NEWS_SELECTOR = 'h2.title.title-color-default a'

    def get_link(self, article):
        return article.get('href')

    def get_headline(self, article):
        return article.string


class WashingtonPostLocators(BaseLocators):
    BASE_URL = 'https://www.washingtonpost.com/'
    NEWS_SELECTOR = 'h2.headline.xx-small.normal-style.text-align-inherit a'

    def get_link(self, article):
        return article.get('href')

    def get_headline(self, article):
        return article.string


class BbcLocators(BaseLocators):
    BASE_URL = 'https://www.bbc.com/'
    NEWS_SELECTOR = 'h3.media__title a.media__link'

    def get_link(self, article):
        return article.get('href')

    def get_headline(self, article):
        return article.string
