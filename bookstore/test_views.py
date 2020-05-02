from rest_framework import status
from rest_framework.test import APITestCase

from bookstore.models import Author, Book


class AuthorViewTest(APITestCase):
    def setUp(self):
        Author.objects.create(name="John Doe")
        Author.objects.create(name="Jane Doe")

    def test_forbid_creation(self):
        author = {"name": "Sample Name"}
        response = self.client.post("/bookstore/authors/", author)
        self.assertEquals(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "Creation via API is not allowed for Authors",
        )

    def test_read_all(self):
        response = self.client.get("/bookstore/authors/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get("count"), 2)

    def test_read_by_id(self):
        response = self.client.get("/bookstore/authors/1", follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get("id"), 1)
        self.assertEquals(response.json().get("name"), "John Doe")

    def test_read_by_name(self):
        response = self.client.get("/bookstore/authors/", {"name": "Jane Doe"})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get("count"), 1)
        self.assertEquals(
            response.json().get("results"), [{"id": 2, "name": "Jane Doe"}]
        )

    def test_forbid_update(self):
        author = {"name": "Sample Name"}
        response = self.client.put(
            "/bookstore/authors/1.json", author, follow=True
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "Update via API is not allowed for Authors",
        )

    def test_forbid_delete(self):
        response = self.client.delete("/bookstore/authors/1.json", follow=True)
        self.assertEquals(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "Delete via API is not allowed for Authors",
        )


class BookViewTest(APITestCase):
    def setUp(self):
        self.john = Author.objects.create(name="John Doe")
        self.jane = Author.objects.create(name="Jane Doe")

        self.red_book = Book.objects.create(
            name="The red book of flames",
            edition="First edition",
            publication_year=1985,
        )
        self.red_book.authors.set([self.jane])

        self.green_book = Book.objects.create(
            name="The green book of trees",
            edition="Second edition",
            publication_year=2010,
        )
        self.green_book.authors.set([self.john, self.jane])

    def test_create_book(self):
        self.assertEquals(Book.objects.count(), 2)
        response = self.client.post(
            "/bookstore/books/",
            {
                "name": "The yellow book",
                "edition": "Third edition",
                "publication_year": 2015,
                "authors": [1],
            },
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Book.objects.count(), 3)

    def test_read_all(self):
        response = self.client.get("/bookstore/books/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get("count"), 2)

    def test_read_by_id(self):
        response = self.client.get("/bookstore/books/1", follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json().get("id"), 1)

    def test_read_by_name(self):
        response = self.client.get(
            "/bookstore/books/", {"name__contains": "red"}
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json().get("results")), 1)
        self.assertEquals(
            response.json().get("results")[0].get("name"),
            "The red book of flames",
        )

    def test_read_by_edition(self):
        response = self.client.get(
            "/bookstore/books/", {"edition": "Second edition"}
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json().get("results")), 1)
        self.assertEquals(
            response.json().get("results")[0].get("edition"), "Second edition"
        )

    def test_read_by_publication_year(self):
        response = self.client.get(
            "/bookstore/books/", {"publication_year": 1985}
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json().get("results")), 1)
        self.assertEquals(
            response.json().get("results")[0].get("publication_year"), 1985
        )

    def test_read_by_publication_year_gt(self):
        response = self.client.get(
            "/bookstore/books/", {"publication_year__gt": 2000}
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json().get("results")), 1)
        self.assertEquals(
            response.json().get("results")[0].get("publication_year"), 2010
        )

    def test_read_by_publication_authors_single(self):
        response = self.client.get("/bookstore/books/", {"authors": 1})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json().get("results")), 1)
        self.assertEquals(response.json().get("results")[0].get("id"), 2)

    def test_read_by_publication_authors_multiple(self):
        response = self.client.get("/bookstore/books/", {"authors": 2})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json().get("results")), 2)
        self.assertEquals(response.json().get("results")[0].get("id"), 1)
        self.assertEquals(response.json().get("results")[1].get("id"), 2)

    def test_read_by_publication_authors_name(self):
        response = self.client.get(
            "/bookstore/books/", {"authors__name": "John Doe"}
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json().get("results")), 1)
        self.assertEquals(response.json().get("results")[0].get("id"), 2)

    def test_update(self):
        response = self.client.put(
            "/bookstore/books/1.json",
            {
                "name": "The red book of flames updated",
                "edition": "First edition updated",
                "publication_year": 1986,
                "authors": [1, 2],
            },
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        json_response = response.json()
        self.assertEquals(
            json_response.get("name"), "The red book of flames updated"
        )
        self.assertEquals(
            json_response.get("edition"), "First edition updated"
        )
        self.assertEquals(json_response.get("publication_year"), 1986)
        self.assertEquals(json_response.get("authors"), [1, 2])

    def test_delete(self):
        self.assertEquals(Book.objects.count(), 2)
        response = self.client.delete("/bookstore/books/1.json", redirect=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Book.objects.count(), 1)
