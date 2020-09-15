from django.shortcuts import render
from .services import get_news_data
from .services import get_search_data


def search(request):
    if 'search_queryset' in request.GET:
        search_data = get_search_data(request, 10, 'ru')
        return render(request, 'news/search.html', context={'countries': search_data})


def main(request):
    news_data = get_news_data(10, 'ru')
    return render(request, 'news/main.html', context={'countries': news_data})


def get_country(request, country_id):
    return


def get_media(request, country_id, media_id):
    return
