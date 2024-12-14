from django.test import TestCase
from movies.models import Comment, Review, User, Genre, Actor, Director, Producer, Writer, Movie
from django.utils import timezone

class CommentModelTest(TestCase):

    def setUp(self):
        # Создаем фильм, пользователя и отзыв для теста
        self.user = User.objects.create_user(username="john_doe", password="password123")
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
        self.review = Review.objects.create(user=self.user, movie=self.movie, rating=5, text="Great movie!")

        # Создаем комментарий
        self.comment = Comment.objects.create(user=self.user, review=self.review, text="I agree with this review!")

    def test_comment_creation(self):
        # Проверяем, что комментарий был создан правильно
        self.assertEqual(self.comment.user.username, "john_doe")
        self.assertEqual(self.comment.review.id, self.review.id)
        self.assertEqual(self.comment.text, "I agree with this review!")
        self.assertTrue(isinstance(self.comment.created_at, timezone.datetime))
        self.assertFalse(self.comment.deleted)

    def test_comment_str_method(self):
        # Проверяем, что метод __str__ возвращает правильную строку для обычного комментария
        self.assertEqual(str(self.comment), "Комментарий от john_doe к отзыву 1")

    def test_deleted_comment_str_method(self):
        # Помечаем комментарий как удаленный
        self.comment.deleted = True
        self.comment.save()

        # Проверяем, что метод __str__ возвращает строку для удаленного комментария
        self.assertEqual(str(self.comment), "Комментарий удален администратором")

    def test_parent_comment(self):
        # Создаем родительский комментарий
        parent_comment = Comment.objects.create(user=self.user, review=self.review, text="I agree!")

        # Создаем дочерний комментарий, который является ответом на родительский
        child_comment = Comment.objects.create(user=self.user, review=self.review, text="Me too!", parent=parent_comment)

        # Проверяем, что дочерний комментарий связан с родительским
        self.assertEqual(child_comment.parent, parent_comment)

    def test_deleted_comment_flag(self):
        # Помечаем комментарий как удаленный
        self.comment.deleted = True
        self.comment.save()

        # Проверяем, что флаг deleted работает корректно
        self.assertTrue(self.comment.deleted)
