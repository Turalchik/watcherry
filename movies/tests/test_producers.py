from django.test import TestCase
from movies.models import Producer

class ProducerModelTest(TestCase):
    
    def setUp(self):
        # Создаем продюсеров для теста
        self.producer1 = Producer.objects.create(name_id="abc123", name="Steven Spielberg")
        self.producer2 = Producer.objects.create(name_id="def456", name="Quentin Tarantino")
        
    def test_producer_creation(self):
        # Проверяем, что продюсеры созданы корректно
        self.assertEqual(self.producer1.name, "Steven Spielberg")
        self.assertEqual(self.producer2.name, "Quentin Tarantino")
        
    def test_producer_str_method(self):
        # Проверяем, что метод __str__ возвращает правильное имя продюсера
        self.assertEqual(str(self.producer1), "Steven Spielberg")
        self.assertEqual(str(self.producer2), "Quentin Tarantino")
        
    def test_unique_name_id(self):
        # Проверяем, что два продюсера не могут иметь одинаковые name_id
        with self.assertRaises(Exception):
            Producer.objects.create(name_id="abc123", name="New Producer")
