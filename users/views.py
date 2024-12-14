from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .serializers import (
    UserSerializer, ProfileSerializer, PasswordChangeSerializer,
    MovieSerializer, RecommendationSerializer
)
from .models import Profile
from movies.models import Movie
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken

# Вход пользователя
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Регистрация пользователя
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({"message": "Регистрация прошла успешно!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Профиль пользователя
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Создание профиля, если он отсутствует
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)

        profile_serializer = ProfileSerializer(user.profile)
        reviews = user.reviews.all()
        reviews_serializer = RecommendationSerializer(reviews, many=True)

        movies_with_reviews = Movie.objects.filter(reviews__user=user).distinct()
        movies_serializer = MovieSerializer(movies_with_reviews, many=True)

        liked_movies = user.profile.liked_movies.all()
        liked_movies_serializer = MovieSerializer(liked_movies, many=True)

        recommendations = get_recommendations(user)
        recommendations_serializer = MovieSerializer(recommendations, many=True)

        return Response({
            "profile": profile_serializer.data,
            "reviews": reviews_serializer.data,
            "movies_with_reviews": movies_serializer.data,
            "liked_movies": liked_movies_serializer.data,
            "recommendations": recommendations_serializer.data,
        })

    def post(self, request):
        profile_serializer = ProfileSerializer(request.user.profile, data=request.data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Смена пароля
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            update_session_auth_hash(request, user)
            return Response({"message": "Пароль успешно изменен!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Рекомендации
class RecommendationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recommendations = get_recommendations(request.user)
        serializer = MovieSerializer(recommendations, many=True)
        return Response(serializer.data)

# Вспомогательная функция для рекомендаций
def get_recommendations(user):
    liked_movies = user.profile.liked_movies.prefetch_related('genres', 'actors').all()
    if not liked_movies:
        return []

    liked_genres = set(genre for movie in liked_movies for genre in movie.genres.all())
    liked_actors = set(actor for movie in liked_movies for actor in movie.actors.all())
    liked_producers = set(producer for movie in liked_movies for producer in movie.producers.all())

    filter_criteria = Q()
    if liked_genres:
        filter_criteria |= Q(genres__in=liked_genres)
    if liked_actors:
        filter_criteria |= Q(actors__in=liked_actors)
    if liked_producers:
        filter_criteria |= Q(producers__in=liked_producers)

    if not filter_criteria:
        return []

    recommendations = Movie.objects.filter(filter_criteria).exclude(id__in=liked_movies).distinct()
    return recommendations
