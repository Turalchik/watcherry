from django.contrib import admin
from .models import Movie, Actor, Director, Producer, Review, Comment

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'rating', 'votes')
    search_fields = ('title',)

admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Producer)
admin.site.register(Review)
admin.site.register(Comment)