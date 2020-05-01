from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255)
    edition = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    authors = models.ManyToManyField(Author)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name
