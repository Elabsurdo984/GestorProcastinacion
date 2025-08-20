import unittest
from src.category_manager import CategoryManager

class TestCategoryManager(unittest.TestCase):
    def setUp(self):
        self.category_manager = CategoryManager()
        
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