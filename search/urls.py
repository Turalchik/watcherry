# search/urls.py
from django.urls import path
from .views import (
    SearchMoviesAPIView,
)

urlpatterns = [
    path('', SearchMoviesAPIView.as_view(), name='api-search-movies'),
]
