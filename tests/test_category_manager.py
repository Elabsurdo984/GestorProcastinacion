import unittest
from datetime import datetime, timedelta
from src.data.category_manager import CategoryManager
from src.models.task import Task, Priority

class TestCategoryManager(unittest.TestCase):
    def setUp(self):
        self.category_manager = CategoryManager()
        self.future_date = datetime.now() + timedelta(days=1)
        
    def test_crear_categoria(self):
        self.category_manager.add_category("Trabajo")
        self.assertIn("Trabajo", self.category_manager.get_categories())
        
    def test_categoria_duplicada(self):
        self.category_manager.add_category("Hogar")
        with self.assertRaises(ValueError):
            self.category_manager.add_category("Hogar")
            
    def test_eliminar_categoria(self):
        self.category_manager.add_category("Temporal")
        self.category_manager.remove_category("Temporal")
        self.assertNotIn("Temporal", self.category_manager.get_categories())
        
    def test_no_eliminar_general(self):
        with self.assertRaises(ValueError):
            self.category_manager.remove_category("General")

    def test_eliminar_categoria_inexistente(self):
        with self.assertRaises(ValueError):
            self.category_manager.remove_category("Inexistente")

    def test_get_category_stats(self):
        self.category_manager.add_category("Personal")
        self.category_manager.add_category("Compras")

        task1 = Task("Comprar leche", "Ir al supermercado", self.future_date, Priority.BAJA, "Compras")
        task1.completed = True
        task1.last_update = datetime.now() - timedelta(minutes=30)

        task2 = Task("Pagar facturas", "Facturas de servicios", self.future_date, Priority.ALTA, "Hogar")
        task2.last_update = datetime.now() - timedelta(days=2) # Procrastinated

        task3 = Task("Estudiar Python", "Capítulo 5", self.future_date, Priority.MEDIA, "Personal")
        task3.last_update = datetime.now() - timedelta(hours=10)

        task4 = Task("Llamar a Juan", "Reunión de proyecto", self.future_date, Priority.ALTA, "Trabajo")
        task4.last_update = datetime.now() - timedelta(minutes=5)

        task5 = Task("Hacer ejercicio", "Rutina diaria", self.future_date, Priority.BAJA, "Personal")
        task5.completed = True
        task5.last_update = datetime.now() - timedelta(days=1) # Procrastinated, but completed

        tasks = [task1, task2, task3, task4, task5]
        stats = self.category_manager.get_category_stats(tasks)

        self.assertIn("Compras", stats)
        self.assertEqual(stats["Compras"]["total"], 1)
        self.assertEqual(stats["Compras"]["completed"], 1)
        self.assertEqual(stats["Compras"]["pending"], 0)
        self.assertEqual(stats["Compras"]["high_priority"], 0)
        self.assertEqual(stats["Compras"]["procrastinated"], 0)

        self.assertIn("Hogar", stats)
        self.assertEqual(stats["Hogar"]["total"], 1)
        self.assertEqual(stats["Hogar"]["completed"], 0)
        self.assertEqual(stats["Hogar"]["pending"], 1)
        self.assertEqual(stats["Hogar"]["high_priority"], 1)
        self.assertEqual(stats["Hogar"]["procrastinated"], 1)

        self.assertIn("Personal", stats)
        self.assertEqual(stats["Personal"]["total"], 2)
        self.assertEqual(stats["Personal"]["completed"], 1)
        self.assertEqual(stats["Personal"]["pending"], 1)
        self.assertEqual(stats["Personal"]["high_priority"], 0)
        self.assertEqual(stats["Personal"]["procrastinated"], 0) # task5 is completed, so not procrastinated

        self.assertIn("Trabajo", stats)
        self.assertEqual(stats["Trabajo"]["total"], 1)
        self.assertEqual(stats["Trabajo"]["completed"], 0)
        self.assertEqual(stats["Trabajo"]["pending"], 1)
        self.assertEqual(stats["Trabajo"]["high_priority"], 1)
        self.assertEqual(stats["Trabajo"]["procrastinated"], 0)
