# search/serializers.py
from rest_framework import serializers
from .models import Movie, Genre, Actor, Director, Producer

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name']

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name']

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)
    directors = DirectorSerializer(many=True)
    producers = ProducerSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'title_id', 'title', 'poster_url', 'release_year',
            'rating', 'votes', 'duration', 'genres', 'actors', 'directors', 'producers'
        ]
