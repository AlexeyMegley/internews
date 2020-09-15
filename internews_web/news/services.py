from collections import defaultdict
from logging import getLogger
from random import shuffle

from .models import Country, Media, Article
from translations.models import Language, TranslatedHeader
from .url_resolvers import UrlParser
from .serializers import CountrySerializer, MediaSerializer, ArticleSerializer


logger = getLogger(__name__)


def save_article(article_url: str, article_header: str, locator_name: str):
    url_parser = UrlParser(article_url)
    try:
        media = Media.objects.get(website__locator_name=locator_name)
    except:
        logger.exception(f"Exception occurred while getting media by locator '{locator_name}'")
        raise
    else:
        header, _ = TranslatedHeader.objects.get_or_create(text=article_header,
                                                           language=media.language)

        article, _ = Article.objects.get_or_create(media=media,
                                                   url=url_parser.get_absolute_url(),
                                                   defaults={'header': header})


def get_news_data(articles_limit: int, language_code: str) -> list:
    """
    :param articles_limit: amount of articles attached to country
    :param language_code: language code
    :return:
    [
        country1: {
           medias: [
                   {
                       articles: [article1, article2...],
                       name: ...,
                       <other media fields>
                   },
                   {
                       articles: [article1, article2...],
                       name: ...,
                       <other media fields>
                   }
           ],
           articles: [article1, article2...],
           name: country_name,
           flag: country_flag
        },
        country2: {
            ...
        },
        ...
    ]
    """
    assert articles_limit > 0, "Limit should be positive integer!"

    media_pk_to_articles = defaultdict(list)
    country_pk_to_medias = defaultdict(list)
    for article in Article.objects.all():
        serialized_article = ArticleSerializer(article).data
        media_pk_to_articles[article.media.pk].append(serialized_article)

    for media in Media.objects.all():
        serialized_media = MediaSerializer(media).data
        media_articles = media_pk_to_articles.get(media.pk, [])
        serialized_media['articles'] = media_articles
        country_pk_to_medias[media.country.pk].append(serialized_media)

    result_data = []
    for country in Country.objects.all():
        serialized_country = CountrySerializer(country).data
        country_medias = country_pk_to_medias.get(country.pk, [])
        serialized_country['medias'] = country_medias

        articles = [media['articles'] for media in country_medias]
        serialized_country['articles'] = shuffle_articles(articles,
                                                          articles_limit)
        result_data.append(serialized_country)

    return result_data


def get_country_data(country_id: int) -> dict:
    """
    :param country_id:
    :return:
    {
        articles: [
            {
               name: <article_name>,
               url: <article url>,
               <other article fields>
            },
            ...
        ],
        name: <media_name>,
        website: <media website>,
        country: <media country>,
        language: <media language>,
        logo: <media logo>
    }
    """
    return {}


def get_media_data(media_id: int) -> dict:
    """
    :param media_id:
    :return:
    {
        articles: [
            {
               articles: [article1, article2...],
               name: ...,
               <other media fields>
            },
            {
               articles: [article3, article4...],
               name: ...,
               <other media fields>
            }
            ...
        ],
        name: <country_name>,
        flag: <flag url>
    }
    """
    return {}


def shuffle_articles(articles: [list], limit: int) -> list:
    # Ignore initial order
    for article_list in articles:
        shuffle(article_list)

    article_groups = len(articles)
    shuffled_articles = []
    article_number = 0
    while any(articles) and limit:
        current_group = articles[article_number % article_groups]
        if current_group:
            shuffled_articles.append(current_group.pop())
            limit -= 1
        article_number += 1

    return shuffled_articles


def get_search_data(request, articles_limit: int, language_code: str):
    """
        :param articles_limit: amount of articles attached to country
        :param language_code: language code
        :return:
        [
            country1: {
               medias: [
                       {
                           articles: [article1, article2...],
                           name: ...,
                           <other media fields>
                       },
                       {
                           articles: [article1, article2...],
                           name: ...,
                           <other media fields>
                       }
               ],
               articles: [article1, article2...],
               name: country_name,
               flag: country_flag
            },
            country2: {
                ...
            },
            ...
        ]
        """
    assert articles_limit > 0, "Limit should be positive integer!"

    media_pk_to_articles = defaultdict(list)
    country_pk_to_medias = defaultdict(list)
    for article in Article.objects.filter(header__text__icontains=request.GET.get('search_queryset')):
        serialized_article = ArticleSerializer(article).data
        media_pk_to_articles[article.media.pk].append(serialized_article)

    for media in Media.objects.all():
        serialized_media = MediaSerializer(media).data
        media_articles = media_pk_to_articles.get(media.pk, [])
        serialized_media['articles'] = media_articles
        country_pk_to_medias[media.country.pk].append(serialized_media)

    result_data = []
    for country in Country.objects.all():
        serialized_country = CountrySerializer(country).data
        country_medias = country_pk_to_medias.get(country.pk, [])
        serialized_country['medias'] = country_medias

        articles = [media['articles'] for media in country_medias]
        serialized_country['articles'] = shuffle_articles(articles,
                                                          articles_limit)
        result_data.append(serialized_country)

    return result_data
