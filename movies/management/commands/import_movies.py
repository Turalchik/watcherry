import csv
import os
import requests
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, Actor, Director, Producer, Writer

class Command(BaseCommand):
    help = 'Import movies from IMDb dataset'
    OMDB_API_KEY = '9639702f'  # Замените на ваш ключ OMDb
    DATA_DIR = os.getenv("DATA_DIR", "/app/data/")  # Путь к папке с данными

    def get_poster_url(self, title):
        url = f'http://www.omdbapi.com/?t={title}&apikey={self.OMDB_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            poster_url = data.get('Poster')
            return poster_url if poster_url and poster_url != 'N/A' else None
        return None

    def movieToDirectorsAndWriters(self, filename):
        movie_to_directors = {}
        movie_to_writers = {}

        with open(os.path.join(self.DATA_DIR, filename), newline='', encoding='utf-8') as crew_file:
            crew_reader = csv.DictReader(crew_file, delimiter='\t')
            for row in crew_reader:
                movie_to_directors[row['tconst']] = row['directors']
                movie_to_writers[row['tconst']] = row['writers']

        return movie_to_directors, movie_to_writers

    def movieToActorsAndProducers(self, filename):
        movie_to_actors = {}
        movie_to_producers = {}

        with open(os.path.join(self.DATA_DIR, filename), newline='', encoding='utf-8') as principals_file:
            principals_reader = csv.DictReader(principals_file, delimiter='\t')
            for row in principals_reader:
                if row['category'] in ['actor', 'actress']:
                    if row['tconst'] not in movie_to_actors:
                        movie_to_actors[row['tconst']] = []
                    movie_to_actors[row['tconst']].append(row['nconst'])
                elif row['category'] == 'producer':
                    if row['tconst'] not in movie_to_producers:
                        movie_to_producers[row['tconst']] = []
                    movie_to_producers[row['tconst']].append(row['nconst'])

        return movie_to_actors, movie_to_producers

    def movieToRating(self, filename):
        movie_to_rating = {}

        with open(os.path.join(self.DATA_DIR, filename), newline='', encoding='utf-8') as ratings_file:
            ratings_reader = csv.DictReader(ratings_file, delimiter='\t')
            for row in ratings_reader:
                movie_to_rating[row['tconst']] = {
                    'averageRating': float(row['averageRating']),
                    'numVotes': int(row['numVotes'])
                }

        return movie_to_rating

    def idToName(self, filename):
        id_to_name = {}

        with open(os.path.join(self.DATA_DIR, filename), newline='', encoding='utf-8') as name_file:
            name_reader = csv.DictReader(name_file, delimiter='\t')
            for row in name_reader:
                id_to_name[row['nconst']] = row['primaryName']

        return id_to_name

    def handle(self, *args, **kwargs):
        movie_to_actors, movie_to_producers = self.movieToActorsAndProducers(filename='title_principals_sample.tsv')
        movie_to_rating = self.movieToRating(filename='title.ratings.tsv')
        id_to_name = self.idToName(filename='name.basics.tsv')
        movie_to_directors, movie_to_writers = self.movieToDirectorsAndWriters(filename='title_crew_sample.tsv')

        self.stdout.write(self.style.SUCCESS("Dicts created successfully!"))

        with open(os.path.join(self.DATA_DIR, 'title_basics_sample.tsv'), newline='', encoding='utf-8') as basics_file:
            basics_reader = csv.DictReader(basics_file, delimiter='\t')
            for row in basics_reader:
                if row['titleType'] == 'movie':
                    title = row['primaryTitle']
                    title_id = row['tconst']
                    rating = movie_to_rating.get(title_id, {}).get('averageRating')
                    votes = movie_to_rating.get(title_id, {}).get('numVotes')
                    release_year = int(row['startYear']) if row['startYear'].isdigit() else None
                    poster_url = self.get_poster_url(row['primaryTitle'])
                    duration = int(row['runtimeMinutes']) if row['runtimeMinutes'].isdigit() else None

                    movie, created = Movie.objects.update_or_create(
                        title_id=title_id,  # Уникальный идентификатор фильма
                        defaults={
                            'title': title,
                            'release_year': release_year,
                            'rating': rating,
                            'votes': votes,
                            'poster_url': poster_url,
                            'duration': duration,
                        }
                    )

                    if row['genres'] and row['genres'] != '\\N':
                        genres = row['genres'].split(',')
                        for genre_name in genres:
                            genre, created = Genre.objects.get_or_create(name=genre_name.strip())
                            movie.genres.add(genre)

                    if title_id in movie_to_actors:
                        for actor_id in movie_to_actors[title_id]:
                            if actor_id not in id_to_name:
                                continue

                            actor_name = id_to_name[actor_id]
                            actor, created = Actor.objects.get_or_create(name_id=actor_id, name=actor_name)
                            movie.actors.add(actor)

                    if title_id in movie_to_directors:
                        if movie_to_directors[title_id] != '\\N':
                            for director_id in movie_to_directors[title_id].split(','):
                                if director_id not in id_to_name:
                                    continue

                                director_name = id_to_name[director_id]
                                director, created = Director.objects.get_or_create(name_id=director_id, name=director_name)
                                movie.directors.add(director)

                        if movie_to_writers[title_id] != '\\N':
                            for writer_id in movie_to_writers[title_id].split(','):
                                if writer_id not in id_to_name:
                                    continue

                                writer_name = id_to_name[writer_id]
                                writer, created = Writer.objects.get_or_create(name_id=writer_id, name=writer_name)
                                movie.writers.add(writer)

                    if title_id in movie_to_producers:
                        for producer_id in movie_to_producers[title_id]:
                            if producer_id not in id_to_name:
                                continue

                            producer_name = id_to_name[producer_id]
                            producer, created = Producer.objects.get_or_create(name_id=producer_id, name=producer_name)
                            movie.producers.add(producer)

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
