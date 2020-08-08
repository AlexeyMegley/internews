from django.shortcuts import render
from .models import Article


def main(request):
    return render(request, 'main/main.html', context={'articles': Article.objects.all()})


def russia(request):
    return render(request, 'main/main.html', context={'articles': Article.objects.filter(media__country__id='1')})


def usa(request):
    return render(request, 'main/main.html', context={'articles': Article.objects.filter(media__country__id='2')})
