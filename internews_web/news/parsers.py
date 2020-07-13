import requests
from bs4 import BeautifulSoup


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
                headline_headline_link.append(((article.string).replace('\n', '')).strip())
                if article.get('href').find('http') >= 0:
                    headline_headline_link.append(article.get('href'))
                else:
                    headline_headline_link.append((f'{url}' + article.get('href')))
                result.append(headline_headline_link)
        return result

    def get_page_html(self, url: str):
        return requests.get(url)

    def soup(self, url):
        return BeautifulSoup(self.get_page_html(url).text, 'html.parser')
