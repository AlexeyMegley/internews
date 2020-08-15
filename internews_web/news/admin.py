from django.contrib import admin
from .models import Media, Article, Country, Website
from translations.models import Language, TranslatedHeader

admin.site.register(Media)
admin.site.register(Website)
admin.site.register(Article)
admin.site.register(Country)
admin.site.register(Language)
admin.site.register(TranslatedHeader)
