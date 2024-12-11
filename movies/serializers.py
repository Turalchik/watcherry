from rest_framework import serializers
from .models import Movie, Review, Comment

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title_id', 'title', 'poster_url', 'release_year', 'rating', 'votes']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'content', 'rating', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'content', 'parent', 'created_at']
