from rest_framework import viewsets

from bookstore.models import Author, Book
from bookstore.serializers import AuthorSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = ["name", "publication_year", "edition", "authors"]


class AuthorsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_fields = ["name"]
