from logging import getLogger

from .models import Country, Media, Article
from translations.models import Language, TranslatedHeader
from .url_resolvers import UrlParser
from .locators import *

logger = getLogger(__name__)


def save_article(article_url: str, article_header: str):
    url_parser = UrlParser(article_url)
    try:
        media = Media.objects.get(website_url=url_parser.get_base_url())
    except:
        logger.exception(f"Exception occurred while getting media by url {article_url}")
        raise
    else:
        header = TranslatedHeader.objects.create(header=article_header, language=media.language)
        header.save()
        article, created = Article.objects.get_or_create(media=media, relative_link=url_parser.get_relative_url(),
                                                         header=header)
        article.save()
