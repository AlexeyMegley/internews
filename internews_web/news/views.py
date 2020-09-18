from django.shortcuts import render
from django.http import Http404
from .services import get_news_data, get_country_data, get_media_data, \
    get_search_data


def search(request):
    if 'search_string' in request.GET:
        search_string = request.GET['search_string']
        search_data = get_search_data(search_string, 'ru')
        return render(request, 'news/search.html',
                      context={'articles': search_data,
                               'search_string': search_string})
    return Http404("Nothing to search")


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
