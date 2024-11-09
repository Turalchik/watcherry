import csv
import requests
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, Actor

class Command(BaseCommand):
    help = 'Import movies from IMDb dataset'

    OMDB_API_KEY = '9639702f'  # Замените на ваш ключ OMDb

    def get_poster_url(self, title):
        url = f'http://www.omdbapi.com/?t={title}&apikey={self.OMDB_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            poster_url = data.get('Poster')
            return poster_url if poster_url and poster_url != 'N/A' else None
        return None

    def handle(self, *args, **kwargs):
        with open('/home/turalchik/web/project/watcherry/small_sample.tsv', newline='', encoding='utf-8') as basics_file, \
             open('/home/turalchik/web/project/watcherry/title.ratings.tsv', newline='', encoding='utf-8') as ratings_file, \
             open('/home/turalchik/web/project/watcherry/title.principals.tsv', newline='', encoding='utf-8') as principals_file:
            
            basics_reader = csv.DictReader(basics_file, delimiter='\t')
            ratings_reader = csv.DictReader(ratings_file, delimiter='\t')
            principals_reader = csv.DictReader(principals_file, delimiter='\t')

            ratings_data = {row['tconst']: row for row in ratings_reader}

            # Собираем информацию об актёрах
            actors_data = {}
            for row in principals_reader:
                if row['category'] == 'actor' or row['category'] == 'actress':  # Фильтруем только актёров и актрис
                    title_id = row['tconst']
                    if title_id not in actors_data:
                        actors_data[title_id] = []
                    actors_data[title_id].append(row['nconst'])  # Добавляем ID актёра

            for row in basics_reader:
                if row['titleType'] == 'movie':
                    rating_data = ratings_data.get(row['tconst'])
                    if rating_data:
                        release_year = int(row['startYear']) if row['startYear'].isdigit() else None

                        poster_url = self.get_poster_url(row['primaryTitle'])

                        # Используем update_or_create вместо create
                        movie, created = Movie.objects.update_or_create(
                            title_id=row['tconst'],  # Уникальный идентификатор фильма
                            defaults={
                                'title': row['primaryTitle'],
                                'release_year': release_year,
                                'rating': float(rating_data['averageRating']),
                                'votes': int(rating_data['numVotes']),
                                'poster_url': poster_url,
                            }
                        )

                        # Добавляем жанры
                        if row['genres'] and row['genres'] != '\\N':
                            genres = row['genres'].split(',')
                            for genre_name in genres:
                                genre, created = Genre.objects.get_or_create(name=genre_name.strip())
                                movie.genres.add(genre)

                        # Добавляем актёров
                        actor_ids = actors_data.get(row['tconst'], [])
                        for actor_id in actor_ids:
                            actor_name = actor_id  # Предположим, что в другой таблице можно соотнести имя по `nconst`
                            actor, created = Actor.objects.get_or_create(name=actor_name)
                            movie.actors.add(actor)

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
