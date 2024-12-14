from django.test import TestCase
from movies.models import Director

class DirectorModelTest(TestCase):
    
    def setUp(self):
        # Создаем директоров для теста
        self.director1 = Director.objects.create(name_id="12345", name="Christopher Nolan")
        self.director2 = Director.objects.create(name_id="67890", name="Quentin Tarantino")
        
    def test_director_creation(self):
        # Проверяем, что директора созданы корректно
        self.assertEqual(self.director1.name, "Christopher Nolan")
        self.assertEqual(self.director2.name, "Quentin Tarantino")
        
    def test_director_str_method(self):
        # Проверяем, что метод __str__ возвращает правильное имя директора
        self.assertEqual(str(self.director1), "Christopher Nolan")
        self.assertEqual(str(self.director2), "Quentin Tarantino")
        
    def test_unique_name_id(self):
        # Проверяем, что два директора не могут иметь одинаковые name_id
        with self.assertRaises(Exception):
            Director.objects.create(name_id="12345", name="New Director")
