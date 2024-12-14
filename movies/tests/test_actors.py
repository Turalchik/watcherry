from django.test import TestCase
from movies.models import Actor

class ActorModelTest(TestCase):
    
    def setUp(self):
        # Создаем актеров для теста
        self.actor1 = Actor.objects.create(name_id="12345", name="Leonardo DiCaprio")
        self.actor2 = Actor.objects.create(name_id="67890", name="Joseph Gordon-Levitt")
        
    def test_actor_creation(self):
        # Проверяем, что актеры созданы корректно
        self.assertEqual(self.actor1.name, "Leonardo DiCaprio")
        self.assertEqual(self.actor2.name, "Joseph Gordon-Levitt")
        
    def test_actor_str_method(self):
        # Проверяем, что метод __str__ возвращает правильное имя актера
        self.assertEqual(str(self.actor1), "Leonardo DiCaprio")
        self.assertEqual(str(self.actor2), "Joseph Gordon-Levitt")
        
    def test_actor_str_method_no_name(self):
        # Проверяем, что если у актера нет имени, то возвращается "Unnamed Actor"
        actor3 = Actor.objects.create(name_id="11223")
        self.assertEqual(str(actor3), "Unnamed Actor")

    def test_unique_name_id(self):
        # Проверяем, что два актера не могут иметь одинаковые name_id
        with self.assertRaises(Exception):
            Actor.objects.create(name_id="12345", name="New Actor")
