from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
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


class MovieDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, title_id):
        movie = get_object_or_404(Movie, title_id=title_id)
        reviews = movie.reviews.prefetch_related('comments')
        movie_serializer = MovieSerializer(movie)
        review_serializer = ReviewSerializer(reviews, many=True)
        
        is_authenticated = request.user.is_authenticated
        user_has_reviewed = reviews.filter(user=request.user).exists() if is_authenticated else False
                
        liked = False
        if is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile:
                liked = profile.liked_movies.filter(id=movie.id).exists()
        
        data = {
            'movie': movie_serializer.data,
            'reviews': review_serializer.data,
            'isAuthenticated': is_authenticated,
            'userHasReviewed': user_has_reviewed,
            'liked': liked,
        }
        return Response(data, status=200)


class SearchMoviesAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            movies = Movie.objects.filter(title__icontains=query)
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
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


class CommentListCreateAPIView(APIView):
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
