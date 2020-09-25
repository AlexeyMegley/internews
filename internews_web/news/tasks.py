from logging import getLogger

from django.conf import settings

from internews_web.celery import app
from .locators import active_locators
from .parsers import BaseStaticParser
from .services import save_article, cleanup_articles

logger = getLogger(__name__)


@app.task
def parse_static_websites():
    logger.info("Start parsing...")
    failed_urls = []
    for locator_cls in active_locators:
        current_url, link, headline = locator_cls.get_full_news_path(), "", ""
        logger.info(f"Start parsing '{current_url}' with '{locator_cls.__name__}'")
        try:
            base_static_parser = BaseStaticParser(locator_cls())
            for link, headline in base_static_parser.get_articles_data():
                save_article(link, headline, locator_cls.__name__)
        except:
            logger.exception(f"Exception occurred while parsing '{current_url}'!\n"
                             f"Link: '{link}', headline: '{headline}'")
            failed_urls.append(current_url)

    successful_urls = [locator_cls.get_full_news_path() for locator_cls in active_locators
                       if locator_cls.get_full_news_path() not in failed_urls]
    report_msg = f"Parsing was finished!\n" \
                 f"Successfully parsed urls: {successful_urls}\n" \
                 f"Failed urls: {failed_urls}"

    if failed_urls:
        logger.error("Attention! Some urls haven't been parsed!")
        logger.error(report_msg)
    else:
        logger.info(report_msg)


@app.task
def remove_old_articles():
    logger.info("Deleting old articles...")
    cleanup_articles(settings.ARTICLE_EXPIRED_THRESHOLD_DAYS)
    logger.info("Articles deleted!")
