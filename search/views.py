# search/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer


class SearchMoviesAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            movies = Movie.objects.filter(title__icontains=query)
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Введите запрос для поиска."}, status=status.HTTP_400_BAD_REQUEST)