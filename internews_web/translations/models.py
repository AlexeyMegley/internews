from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name


class TranslatedHeader(models.Model):
    header = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    # translations = models.ManyToManyField("self")

    def __str__(self):
        return f"{self.header} ({self.language})"
