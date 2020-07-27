from abc import ABC, abstractmethod
from .url_resolvers import UrlParser


active_locators = []


def register_locator(cls):
    is_abstract = hasattr(cls, "__abstractmethods__") and len(cls.__abstractmethods__)
    if cls not in active_locators and not is_abstract:
        active_locators.append(cls)


class BaseLocator(ABC):
    BASE_URL = ''
    NEWS_URL_PATH = ''
    NEWS_SELECTOR = ''

    @classmethod
    def get_full_news_path(cls):
        return UrlParser.join_urls(cls.BASE_URL, cls.NEWS_URL_PATH)

    @abstractmethod
    def get_raw_headline(self, article) -> str:
        pass

    @abstractmethod
    def get_raw_link(self, article) -> str:
        pass

    def handle_headline(self, raw_headline: str):
        return raw_headline.strip()

    def handle_link(self, raw_link: str):
        return self.ensure_url_is_absolute(raw_link.strip())

    def get_link(self, article):
        raw_link = self.get_raw_link(article)
        return self.handle_link(raw_link)

    def get_headline(self, article):
        raw_headline = self.get_raw_headline(article)
        return self.handle_headline(raw_headline)

    def ensure_url_is_absolute(self, url):
        if UrlParser.url_is_absolute(url):
            return url
        return UrlParser.join_urls(self.BASE_URL, url)


@register_locator
class RussiaTodayLocator(BaseLocator):
    BASE_URL = 'https://russian.rt.com/'
    NEWS_SELECTOR = 'div.card__heading.card__heading_main-news a'

    def get_raw_link(self, article):
        return article.get('href')

    def get_raw_headline(self, article):
        return article.string


@register_locator
class RiaLocator(BaseLocator):
    BASE_URL = 'https://ria.ru/'
    NEWS_SELECTOR = 'span.elem-info__share .share'

    def get_raw_link(self, article):
        return article.get('data-url')

    def get_raw_headline(self, article):
        return article.get('data-title')


@register_locator
class RainLocator(BaseLocator):
    BASE_URL = 'https://tvrain.ru/'
    NEWS_URL_PATH = 'news'
    NEWS_SELECTOR = 'h3 a'

    def get_raw_link(self, article):
        return article.get('href')

    def get_raw_headline(self, article):
        return article.string


@register_locator
class FoxNewsLocator(BaseLocator):
    BASE_URL = 'https://www.foxnews.com/'
    NEWS_SELECTOR = 'h2.title.title-color-default a'

    def get_raw_link(self, article):
        return article.get('href')

    def get_raw_headline(self, article):
        return article.string


@register_locator
class WashingtonPostLocator(BaseLocator):
    BASE_URL = 'https://www.washingtonpost.com/'
    NEWS_SELECTOR = 'h2.headline.xx-small.normal-style.text-align-inherit a'

    def get_raw_link(self, article):
        return article.get('href')

    def get_raw_headline(self, article):
        return article.string


@register_locator
class BbcLocator(BaseLocator):
    BASE_URL = 'https://www.bbc.com/'
    NEWS_SELECTOR = 'h3.media__title a.media__link'

    def get_raw_link(self, article):
        return article.get('href')

    def get_raw_headline(self, article):
        return article.string
