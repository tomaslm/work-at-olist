from django.db import models


class Author(models.Model):
    name = models.CharField(
        max_length=255, unique=True, null=False, blank=False,
    )

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    edition = models.CharField(max_length=255, blank=True)
    publication_year = models.IntegerField(null=False)
    authors = models.ManyToManyField(Author)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name
