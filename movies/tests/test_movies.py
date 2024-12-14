from django.test import TestCase
from movies.models import Movie, Genre, Actor, Director, Producer, Writer

class MovieModelTest(TestCase):
    def setUp(self):
        # Создание связанных объектов
        self.genre1 = Genre.objects.create(name="Action")
        self.genre2 = Genre.objects.create(name="Sci-Fi")
        self.actor1 = Actor.objects.create(name_id="12345", name="Leonardo DiCaprio")
        self.actor2 = Actor.objects.create(name_id="67890", name="Joseph Gordon-Levitt")
        self.director = Director.objects.create(name="Christopher Nolan")
        self.producer = Producer.objects.create(name="Emma Thomas")
        self.writer = Writer.objects.create(name="Jonathan Nolan")

        # Создание объекта Movie
        self.movie = Movie.objects.create(
            title="Inception",
            release_year=2010,
            rating=8.8,
            votes=20000,
            duration=148,
            title_id="tt1375666",
            poster_url="http://www.impawards.com/2010/posters/inception_ver3.jpg"
        )

        # Добавление связей ManyToMany
        self.movie.genres.add(self.genre1, self.genre2)
        self.movie.actors.add(self.actor1, self.actor2)
        self.movie.directors.add(self.director)
        self.movie.producers.add(self.producer)
        self.movie.writers.add(self.writer)

    def test_movie_creation(self):
        # Проверка, что объект был создан
        self.assertEqual(self.movie.title, "Inception")
        self.assertEqual(self.movie.release_year, 2010)
        self.assertEqual(self.movie.rating, 8.8)
        self.assertEqual(self.movie.votes, 20000)
        self.assertEqual(self.movie.duration, 148)
        self.assertEqual(self.movie.title_id, "tt1375666")
        self.assertEqual(self.movie.poster_url, "http://www.impawards.com/2010/posters/inception_ver3.jpg")

    def test_genres_association(self):
        # Проверка связи ManyToMany с жанрами
        self.assertIn(self.genre1, self.movie.genres.all())
        self.assertIn(self.genre2, self.movie.genres.all())

    def test_actors_association(self):
        # Проверка связи ManyToMany с актерами
        self.assertIn(self.actor1, self.movie.actors.all())
        self.assertIn(self.actor2, self.movie.actors.all())

    def test_directors_association(self):
        # Проверка связи ManyToMany с режиссерами
        self.assertIn(self.director, self.movie.directors.all())

    def test_producers_association(self):
        # Проверка связи ManyToMany с продюсерами
        self.assertIn(self.producer, self.movie.producers.all())

    def test_writers_association(self):
        # Проверка связи ManyToMany с писателями
        self.assertIn(self.writer, self.movie.writers.all())

    def test_movie_str(self):
        # Проверка строки представления объекта
        self.assertEqual(str(self.movie), "Inception")
