from django.shortcuts import render
from .services import get_news_data, get_country_data, get_media_data


def main(request):
    news_data = get_news_data(10, 'ru')
    return render(request, 'news/main.html', context={'countries': news_data})


def get_country(request, country_id):
    country_data = get_country_data(country_id, 10, 'ru')
    return render(request, 'news/country.html',
                  context={'country': country_data})


def get_media(request, media_id):
    media_data = get_media_data(media_id, 10, 'ru')
    return render(request, 'news/media.html', context={'media': media_data})
