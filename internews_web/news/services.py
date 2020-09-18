from django.db.models import Q
from logging import getLogger

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
                       <media fields>
                   },
                   {
                       <media fields>
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

    serialized_countries = []
    countries = Country.objects.all()
    for country in countries:
        serialized_country = CountrySerializer(country).data
        serialized_countries.append(serialized_country)

    medias = Media.objects.select_related('country', 'language', 'website').all()
    serialized_medias = []
    for media in medias:
        serialized_media = MediaSerializer(media).data
        serialized_medias.append(serialized_media)
        for country in serialized_countries:
            if media.country.pk == country['id']:
                if not 'medias' in country:
                    country['medias'] = [serialized_media]
                else:
                    country['medias'].append(serialized_media)

    for country in serialized_countries:
        articles = Article.objects \
                   .select_related('header', 'media', 'media__country',
                                   'media__language', 'media__website') \
                   .filter(media__country__pk=country['id']) \
                   .order_by('?')[:articles_limit]
        serialized_articles = ArticleSerializer(articles, many=True).data
        country['articles'] = serialized_articles

    return serialized_countries


def get_country_data(country_id: int, articles_limit: int,
                     language_code: str) -> dict:
    """
    :param country_id:
    :param articles_limit:
    :param language_code:
    :return:
    {
        medias: [
            {
                articles: [article1, article2, ...],
                name: <media_name>,
                website: <media website>,
                country: <media country>,
                language: <media language>,
                logo: <media logo>
            },
            ...
        ]
        name: country_name,
        flag: country_flag
    }
    """

    assert articles_limit > 0, "Limit should be positive integer!"
    assert country_id, "Country id should be set!"

    country = Country.objects.get(id=country_id)
    serialized_country = CountrySerializer(country).data
    serialized_country['medias'] = []

    medias = Media.objects.select_related('country', 'language', 'website')\
        .filter(country=country)
    for media in medias:
        serialized_media = MediaSerializer(media).data
        articles = Article.objects \
            .select_related('media', 'header', 'media__website',
                            'media__country', 'media__language') \
            .filter(media=media).order_by('?')[:articles_limit]
        serialized_articles = ArticleSerializer(articles, many=True).data
        serialized_media['articles'] = serialized_articles
        serialized_country['medias'].append(serialized_media)

    return serialized_country


def get_media_data(media_id: int, articles_limit: int,
                   language_code: str) -> dict:
    """
    :param media_id:
    :param articles_limit:
    :param language_code:
    :return:
    {
        articles: [
            {
               <articles fields>
            },
            {
               <articles fields>
            }
            ...
        ],
        name: <media_name>,
        website: <media website>,
        country: <media country>,
        language: <media language>,
        logo: <media logo>
    }
    """
    assert media_id, "Media id should be set!"
    assert articles_limit > 0, "Limit should be positive integer!"

    media = Media.objects.get(id=media_id)
    articles = Article.objects.filter(media=media).order_by('?')[:articles_limit]
    serialized_media = MediaSerializer(media).data
    serialized_articles = ArticleSerializer(articles, many=True).data
    serialized_media['articles'] = serialized_articles
    return serialized_media


def get_search_data(search_string: str, language_code: str) -> list:
    """
        :param search_string: search pattern
        :param language_code: language code
        :return:
        [
            article1,
            article2,
            ...
        ]
        """
    assert search_string, "Search string cant be empty!"

    search_string = search_string.lower()
    translations = TranslatedHeader.objects.filter(text__icontains=search_string)
    header_text_condition = Q(header__text__icontains=search_string)
    translations_condition = Q(header__in=translations)
    articles = Article.objects.select_related('header', 'media',
                                              'media__country',
                                              'media__language',
                                              'media__website')\
        .filter(header_text_condition | translations_condition)

    serialized_articles = ArticleSerializer(articles, many=True).data
    return serialized_articles
