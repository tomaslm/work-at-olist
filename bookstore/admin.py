from django.contrib import admin

from bookstore.models import Author, Book

admin.site.register(Book)
admin.site.register(Author)
