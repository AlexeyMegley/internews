from django.db import models
from translations.models import Language, TranslatedHeader


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    flag = models.ImageField(upload_to="flags")

    def __str__(self):
        return self.name


class Website(models.Model):
    url = models.URLField(unique=True)
    locator_name = models.CharField(max_length=64, blank=True, null=True)
    is_static = models.BooleanField(default=True)

    def __str__(self):
        return self.url


class Media(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="logos", null=True)
    website = models.OneToOneField(Website, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('website', 'country', 'language')

    def __str__(self):
        return f"{self.name}, {self.country}"


class Article(models.Model):
    url = models.URLField(unique=True, max_length=255)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    header = models.ForeignKey(TranslatedHeader, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.header}, {self.media}"
