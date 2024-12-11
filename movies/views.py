from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Movie, Review, Comment
from .serializers import MovieSerializer, ReviewSerializer, CommentSerializer

class MovieListAPIView(APIView):
    """
    Возвращает список популярных и новых фильмов.
    """
    def get(self, request):
        popular_movies = Movie.objects.order_by('-votes')[:10]
        new_movies = Movie.objects.order_by('-release_year')[:10]
        data = {
            'popular_movies': MovieSerializer(popular_movies, many=True).data,
            'new_movies': MovieSerializer(new_movies, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class MovieDetailAPIView(APIView):
    """
    Возвращает детальную информацию о фильме.
    """
    def get(self, request, title_id):
        movie = get_object_or_404(Movie, title_id=title_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchMoviesAPIView(APIView):
    """
    Обрабатывает поиск фильмов по заголовку.
    """
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            movies = Movie.objects.filter(title__icontains=query)
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Введите запрос для поиска."}, status=status.HTTP_400_BAD_REQUEST)


class ReviewListCreateAPIView(APIView):
    """
    Список отзывов для фильма или создание нового отзыва.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, title_id):
        movie = get_object_or_404(Movie, title_id=title_id)
        reviews = movie.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, title_id):
        movie = get_object_or_404(Movie, title_id=title_id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreateAPIView(APIView):
    """
    Список комментариев для отзыва или добавление нового комментария.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        comments = review.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToggleLikeAPIView(APIView):
    """
    Лайк/дизлайк фильма.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, title_id):
        movie = get_object_or_404(Movie, title_id=title_id)
        profile = request.user.profile
        if movie in profile.liked_movies.all():
            profile.liked_movies.remove(movie)
            return Response({"detail": "Фильм удалён из понравившихся."}, status=status.HTTP_200_OK)
        else:
            profile.liked_movies.add(movie)
            return Response({"detail": "Фильм добавлен в понравившиеся."}, status=status.HTTP_200_OK)
