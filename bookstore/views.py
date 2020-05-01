from rest_framework import viewsets

from bookstore.models import Book
from bookstore.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = ["name", "publication_year", "edition", "authors"]
