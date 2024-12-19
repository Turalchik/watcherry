from django.urls import path
from .views import (
    MovieListAPIView,
    MovieDetailAPIView,
    SearchMoviesAPIView,
    ReviewListCreateAPIView,
    CommentListCreateAPIView,
    ToggleLikeAPIView,
    GenreListAPIView,
)

urlpatterns = [
    path('api/movies/', MovieListAPIView.as_view(), name='api-movie-list'),
    path('api/movies/<str:title_id>/', MovieDetailAPIView.as_view(), name='api-movie-detail'),
    path('api/search/', SearchMoviesAPIView.as_view(), name='api-search-movies'),
    path('api/movies/<str:title_id>/reviews/', ReviewListCreateAPIView.as_view(), name='api-review-list-create'),
    path('api/reviews/<int:review_id>/comments/', CommentListCreateAPIView.as_view(), name='api-comment-list-create'),
    path('api/movies/<str:title_id>/toggle_like/', ToggleLikeAPIView.as_view(), name='api-toggle-like'),
    path('api/genres/', GenreListAPIView.as_view(), name='genre-list'),
]
