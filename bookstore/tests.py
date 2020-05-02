from django.core.validators import ValidationError
from django.test import TestCase

from bookstore.models import Author


class AuthorTest(TestCase):
    def test_simple_valid_name(self):
        Author(name="Sample Name").full_clean()

    def test_should_forbid_null_values(self):
        with self.assertRaises(
            ValidationError,
            msg="Shouldn't be possible create Author with null name",
        ):
            Author(name=None).full_clean()

    def test_should_forbid_blank_name(self):
        with self.assertRaises(
            ValidationError, msg="Shouldn't create author with no name"
        ):
            Author(name="").full_clean()

    def test_should_forbid_long_name(self):
        name = "L" + ("o" * 253) + "ng"
        with self.assertRaises(
            ValidationError,
            msg="Shouldn't create author with long name (+255)",
        ):
            Author(name=name).full_clean()

    def test_should_forbid_two_with_same_name(self):
        Author.objects.create(name="sample")
        with self.assertRaises(
            ValidationError,
            msg="Shouldn't be possible add two authors with same name",
        ):
            Author(name="sample").full_clean()
