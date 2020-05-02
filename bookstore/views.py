from rest_framework import viewsets

from bookstore.models import Author, Book
from bookstore.serializers import AuthorSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = {
        "name": ["icontains", "iexact", "contains", "exact"],
        "publication_year": ["exact", "lte", "lt", "gte", "gt"],
        "edition": ["icontains", "iexact", "contains", "exact"],
        "authors": ["exact"],
        "authors__name": ["icontains", "iexact", "contains", "exact"],
    }


class AuthorsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_fields = ["name"]
