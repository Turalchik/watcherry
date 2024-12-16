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
from rest_framework_simplejwt.authentication import JWTAuthentication


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Расширяем поведение стандартного TokenObtainPairView,
        чтобы вернуть токен в виде `response.token`.
        """
        response = super().post(request, *args, **kwargs)
        
        # Проверяем, что токен получен успешно
        if response.status_code == status.HTTP_200_OK:
            return Response({
                'token': response.data['access'],  # Возвращаем только access_token
            }, status=status.HTTP_200_OK)
        
        return response


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Создаем пользователя и его профиль.
        """
        user = serializer.save()
        Profile.objects.get_or_create(user=user)

    def create(self, request, *args, **kwargs):
        """
        Возвращаем только подтверждение регистрации без токена.
        """
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Регистрация прошла успешно!',
            'username': request.data['username']
        }, status=status.HTTP_201_CREATED)


class ProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        # Возвращаем профиль текущего пользователя
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        user = request.user

        # Получаем сериализаторы
        profile_serializer = self.get_serializer(profile)

        # Отзывы и фильмы с отзывами
        movies_with_reviews = Movie.objects.filter(reviews__user=user).distinct()
        movies_with_reviews_serializer = MovieSerializer(movies_with_reviews, many=True)

        # Понравившиеся фильмы
        liked_movies = profile.liked_movies.all()
        liked_movies_serializer = MovieSerializer(liked_movies, many=True)

        # Рекомендации
        recommendations = get_recommendations(user)
        recommendations_serializer = MovieSerializer(recommendations, many=True)

        # Возвращаем данные
        return Response({
            "profile": profile_serializer.data,
            "movies_with_reviews": movies_with_reviews_serializer.data,
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
