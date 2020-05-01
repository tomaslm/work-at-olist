from django.urls import include, path
from rest_framework.routers import DefaultRouter

from bookstore.views import AuthorsViewSet, BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"authors", AuthorsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
