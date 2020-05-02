from rest_framework import status
from rest_framework.test import APITestCase

from bookstore.models import Author


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
