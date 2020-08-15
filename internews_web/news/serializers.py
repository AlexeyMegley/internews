from rest_framework import serializers
from translations.models import Language
from .models import Country, Media, Article


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class MediaSerializer(serializers.ModelSerializer):
    website = serializers.SerializerMethodField()
    country = CountrySerializer()
    language = LanguageSerializer()

    class Meta:
        model = Media
        fields = ('id', 'name', 'website', 'country', 'language', 'logo')

    def get_website(self, obj):
        return obj.website.url


class ArticleSerializer(serializers.ModelSerializer):
    header = serializers.SerializerMethodField()
    media = MediaSerializer()

    class Meta:
        model = Article
        fields = ('id', 'url', 'created_time', 'header', 'media')

    def get_header(self, obj):
        return obj.header.text
