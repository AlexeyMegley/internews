class RussiaTodayLocators():
    URL = 'https://russian.rt.com/'
    NEWS_SELECTOR = 'div.card__heading.card__heading_main-news a'


class RiaLocators():
    URL = 'https://ria.ru/'
    NEWS_SELECTOR = 'span.elem-info__share .share'
    HEADLINE_SELECTOR = 'data-title'
    HEADLINE_LINK = 'data-url'


class RainLocators():
    URL = 'https://tvrain.ru/news/'
    NEWS_SELECTOR = 'h3 a'


class FoxNewsLocators():
    URL = 'https://www.foxnews.com/'
    NEWS_SELECTOR = 'h2.title.title-color-default a'


class WashingtonPostLocators():
    URL = 'https://www.washingtonpost.com/'
    NEWS_SELECTOR = 'h2.headline.xx-small.normal-style.text-align-inherit a'


class BbcLocators():
    URL = 'https://www.bbc.com/'
    NEWS_SELECTOR = 'h3.media__title a.media__link'
