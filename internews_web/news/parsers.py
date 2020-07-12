import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

# Все селекторы можно вынести в отдельный файл, чтобы не захломлять файл
rt_news_selcetor = 'div.card__heading.card__heading_main-news a'
rt_news_head_selector = 'string'
rt_news_link_selector = 'href'

ria_news_selector = 'span.elem-info__share .share'
ria_news_head_selector = 'data-title'
ria_news_link_selector = 'data-url'

rain_news_selector = 'h3 a'
rain_news_head_selector = 'string'
rain_news_link_selector = 'href'


# # Вариант 1 у нас get_news повторяется из функции в функцию, что не очень хорошо. Можно немного переделать методы,
# вообщем нужно экспертное мнение)


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
            headline_headline_link = []
            headline_headline_link.append(article.string)
            headline_headline_link.append(f'{url}' + article.get('href'))
            result.append(headline_headline_link)
        return result


class RiaNewsParser(AbstractParser):
    def get_news(self, url: str, css_selector: str):
        articles = self.soup(url).select(css_selector)
        result = []
        for article in articles:
            headline_headline_link = []
            headline_headline_link.append(article.get('data-title'))
            headline_headline_link.append(article.get('data-url'))
            result.append(headline_headline_link)
        return result


class RainNewsParser(AbstractParser):
    def get_news(self, url: str, css_selector: str):
        articles = self.soup(url).select(css_selector)
        result = []
        for article in articles:
            headline_headline_link = []
            headline_headline_link.append(article.string)
            headline_headline_link.append((f'{url}' + article.get('href')))
            result.append(headline_headline_link)
        return result

# Вариант 2 имеем более универсальный парсер в который мы передаём два либо 4 аргумента в зависимости от сайта,
# большинство сайтов можно будет парсить, ту же медузу, единственое она вроде как динамически подгружается.


class BaseParser():
    def get_news(self, url: str, news_css_selector: str, headline_css_selector=None, headline_link_css_selector=None):
        articles = self.soup(url).select(news_css_selector)
        result = []
        for article in articles:
            headline_headline_link = []
            if headline_css_selector and headline_link_css_selector:
                headline_headline_link.append(article.get(headline_css_selector))
                headline_headline_link.append(article.get(headline_link_css_selector))
                result.append(headline_headline_link)
            else:
                headline_headline_link.append(article.string)
                headline_headline_link.append((f'{url}' + article.get('href')))
                result.append(headline_headline_link)
        return result

    def get_page_html(self, url: str):
        return requests.get(url)

    def soup(self, url):
        return BeautifulSoup(self.get_page_html(url).text, 'html.parser')


bp = BaseParser()
print(bp.get_news('https://russian.rt.com/', 'div.card__heading.card__heading_main-news a'))
