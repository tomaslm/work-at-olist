from rest_framework import serializers

from bookstore.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "name",
            "edition",
            "publication_year",
            "authors",
        ]
