from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import (
    UserSerializer, ProfileSerializer, PasswordChangeSerializer,
    MovieSerializer, RecommendationSerializer
)
from .models import Profile
from movies.models import Movie
from django.db.models import Q


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Profile.objects.get_or_create(user=user)

    def create(self, request, *args, **kwargs):
        """
        Переопределенный метод create для возврата токена после регистрации
        """
        response = super().create(request, *args, **kwargs)  # Создаем пользователя
        user = User.objects.get(username=request.data['username'])  # Получаем пользователя по имени
        refresh = RefreshToken.for_user(user)  # Создаем токен для пользователя
        access_token = str(refresh.access_token)  # Доступ к токену
        return Response({
            'token': access_token,  # Возвращаем токен
            'username': user.username  # Возвращаем имя пользователя
        }, status=status.HTTP_201_CREATED)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get(self, request, *args, **kwargs):
        profile_serializer = self.get_serializer(self.get_object())
        user = request.user

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


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RecommendationsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MovieSerializer

    def get_queryset(self):
        return get_recommendations(self.request.user)


def get_recommendations(user):
    liked_movies = user.profile.liked_movies.prefetch_related('genres', 'actors').all()
    if not liked_movies:
        return []

    liked_genres = {genre for movie in liked_movies for genre in movie.genres.all()}
    liked_actors = {actor for movie in liked_movies for actor in movie.actors.all()}
    liked_producers = {producer for movie in liked_movies for producer in movie.producers.all()}

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
