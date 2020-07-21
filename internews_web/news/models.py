from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

    # TODO - add 'name', 'code' constraint

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255)
    flag = models.ImageField(upload_to="flags")

    # TODO - add 'name' constraint

    def __str__(self):
        return self.name


class Media(models.Model):
    website_url = models.URLField()
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    # TODO - add website_url constraint

    def __str__(self):
        return "{}, {}".format(self.name, self.country)


class Article(models.Model):
    header = models.TextField()
    relative_link = models.URLField()
    created_time = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    # TODO - add media, relative_link constraint

    def __str__(self):
        return "{}, {}".format(self.header, self.media)

