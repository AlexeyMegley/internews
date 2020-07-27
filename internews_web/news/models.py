from django.db import models
from translations.models import Language, TranslatedHeader


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    flag = models.ImageField(upload_to="flags")

    def __str__(self):
        return self.name


class Media(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website_url = models.URLField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('website_url', 'country', 'language')

    def __str__(self):
        return f"{self.name}, {self.country}"


class Article(models.Model):
    relative_link = models.URLField()
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    header = models.ForeignKey(TranslatedHeader, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('media', 'relative_link')

    def __str__(self):
        return f"{self.header}, {self.media}"
