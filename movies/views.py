from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .models import Movie, Review, Comment
from .serializers import MovieSerializer, ReviewSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

class MovieListAPIView(APIView):
    def get(self, request):
        popular_movies = Movie.objects.order_by('-votes')[:10]
        new_movies = Movie.objects.order_by('-release_year')[:10]
        data = {
            'popular_movies': MovieSerializer(popular_movies, many=True).data,
            'new_movies': MovieSerializer(new_movies, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)


from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Movie
from .serializers import MovieSerializer, ReviewSerializer

class MovieDetailAPIView(APIView):
    # Убираем JWT аутентификацию для GET-запросов (она необходима только для создания/изменения)
    authentication_classes = []  # Здесь не требуется аутентификация для GET-запросов
    permission_classes = [AllowAny]  # Разрешаем доступ всем пользователям для просмотра фильма

    def get(self, request, title_id):
        movie = get_object_or_404(Movie, title_id=title_id)
        reviews = movie.reviews.prefetch_related('comments')  # Предзагрузка комментариев для оптимизации
        movie_serializer = MovieSerializer(movie)
        review_serializer = ReviewSerializer(reviews, many=True)

        is_authenticated = request.user.is_authenticated
        user_has_reviewed = reviews.filter(user=request.user).exists() if is_authenticated else False

        liked = False
        if is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile:
                liked = profile.liked_movies.filter(id=movie.id).exists()

        # Добавляем `votes_from_website` и `rating_from_website`
        data = {
            'movie': {
                **movie_serializer.data,
                'votesFromWebsite': movie.votes_from_website,
                'ratingFromWebsite': movie.rating_from_website,
            },
            'reviews': review_serializer.data,
            'isAuthenticated': is_authenticated,
            'userHasReviewed': user_has_reviewed,
            'liked': liked,
        }
        return Response(data, status=200)


class SearchMoviesAPIView(APIView):
    def get(self, request):
        title = request.GET.get('title', '')
        min_rating = request.GET.get("min_rating", None)
        genre = request.GET.get('genre', None)
        
        if title and min_rating and genre:
            movies = Movie.objects.filter(Q(title__icontains=title) & Q(rating_from_website__gte=min_rating) & Q(genres__name__icontains=genre))
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif title and min_rating:
            movies = Movie.objects.filter(Q(title__icontains=title) & Q(rating_from_website__gte=min_rating))
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif title and genre:
            movies = Movie.objects.filter(Q(title__icontains=title) & Q(genres__name__icontains=genre))
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif title:
            movies = Movie.objects.filter(Q(title__icontains=title))
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif not title:
            return Response({"detail": "Введите название для поиска."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Введите запрос для поиска."}, status=status.HTTP_400_BAD_REQUEST)


class ReviewListCreateAPIView(APIView):
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Comment, Review, Genre
from .serializers import CommentSerializer, GenreSerializer


class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        comments = review.comments.filter(parent__isnull=True)  # Получаем только корневые комментарии
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        
        # Получаем данные из запроса
        parent_comment_id = request.data.get('parent', None)  # Получаем ID родительского комментария
        parent_comment = None

        # Если есть родительский комментарий, находим его
        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, id=parent_comment_id)

        # Серилизуем данные комментария
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем новый комментарий, связываем его с родительским, если он есть
            serializer.save(user=request.user, review=review, parent=parent_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToggleLikeAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request, title_id, *args, **kwargs):
        profile = request.user.profile

        try:
            movie = Movie.objects.get(title_id=title_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Фильм с указанным title_id не найден.'}, status=status.HTTP_404_NOT_FOUND)

        if movie in profile.liked_movies.all():
            profile.liked_movies.remove(movie)
            return Response({'message': 'Фильм удалён из списка понравившихся.'}, status=status.HTTP_200_OK)
        else:
            profile.liked_movies.add(movie)
            return Response({'message': 'Фильм добавлен в список понравившихся.'}, status=status.HTTP_200_OK)


class GenreListAPIView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)