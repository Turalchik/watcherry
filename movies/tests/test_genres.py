from django.test import TestCase
from movies.models import Genre

class GenreModelTest(TestCase):
    def setUp(self):
        # Создаем жанры для теста
        self.genre1 = Genre.objects.create(name="Action")
        self.genre2 = Genre.objects.create(name="Comedy")
        
    def test_genre_creation(self):
        # Проверяем, что жанры созданы корректно
        self.assertEqual(self.genre1.name, "Action")
        self.assertEqual(self.genre2.name, "Comedy")
        
    def test_genre_str_method(self):
        # Проверяем, что метод __str__ возвращает правильное имя жанра
        self.assertEqual(str(self.genre1), "Action")
        self.assertEqual(str(self.genre2), "Comedy")

