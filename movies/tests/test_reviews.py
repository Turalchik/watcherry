from django.test import TestCase
from movies.models import Review, Movie, User
from django.utils import timezone

class ReviewModelTest(TestCase):
    
    def setUp(self):
        # Создаем пользователя и фильм для теста
        self.user = User.objects.create_user(username="john_doe", password="password123")
        self.movie = Movie.objects.create(title="Inception", release_year=2010, title_id="inception_2010")
        
        # Создаем отзыв
        self.review1 = Review.objects.create(user=self.user, movie=self.movie, rating=5, text="Great movie!")
        
    def test_review_creation(self):
        # Проверяем, что отзыв был создан правильно
        self.assertEqual(self.review1.user.username, "john_doe")
        self.assertEqual(self.review1.movie.title, "Inception")
        self.assertEqual(self.review1.rating, 5)
        self.assertEqual(self.review1.text, "Great movie!")
        self.assertTrue(isinstance(self.review1.created_at, timezone.datetime))
        
    def test_review_str_method(self):
        # Проверяем, что метод __str__ возвращает правильную строку
        self.assertEqual(str(self.review1), "Review by john_doe for Inception")
        
    def test_unique_user_movie(self):
        # Проверяем, что пользователь не может оставить два отзыва на один фильм
        with self.assertRaises(Exception):
            Review.objects.create(user=self.user, movie=self.movie, rating=4, text="Not bad, but could be better.")
