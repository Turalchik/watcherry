from django.test import TestCase
from movies.models import Writer

class WriterModelTest(TestCase):
    
    def setUp(self):
        # Создаем писателей для теста
        self.writer1 = Writer.objects.create(name_id="12345", name="J.K. Rowling")
        self.writer2 = Writer.objects.create(name_id="67890", name="George R.R. Martin")
        
    def test_writer_creation(self):
        # Проверяем, что писатели созданы корректно
        self.assertEqual(self.writer1.name, "J.K. Rowling")
        self.assertEqual(self.writer2.name, "George R.R. Martin")
        
    def test_writer_str_method(self):
        # Проверяем, что метод __str__ возвращает правильное имя писателя
        self.assertEqual(str(self.writer1), "J.K. Rowling")
        self.assertEqual(str(self.writer2), "George R.R. Martin")
        
    def test_unique_name_id(self):
        # Проверяем, что два писателя не могут иметь одинаковые name_id
        with self.assertRaises(Exception):
            Writer.objects.create(name_id="12345", name="New Writer")
