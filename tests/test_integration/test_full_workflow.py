import unittest
from datetime import datetime, timedelta
from src.models.task import Task, Priority
from src.data.storage import Storage
from src.data.category_manager import CategoryManager

class TestFullWorkflow(unittest.TestCase):
    def setUp(self):
        self.storage = Storage("test_integration.json")
        self.category_manager = CategoryManager()
        # Usar una fecha futura para evitar errores de validación
        self.future_date = datetime.now() + timedelta(days=1)
        
    def test_flujo_completo(self):
        # 1. Crear categoría
        self.category_manager.add_category("Proyecto")
        self.assertIn("Proyecto", self.category_manager.get_categories())
        
        # 2. Crear y guardar tarea
        tarea = Task("Integración", "Test completo", self.future_date, Priority.ALTA)
        self.storage.save_task(tarea)
        
        # 3. Actualizar progreso
        tarea.update_progress(50)
        self.storage.update_task(tarea)
        
        # 4. Verificar estado final
        tareas = self.storage.load_tasks()
        self.assertEqual(len(tareas), 1)
        tarea_cargada = next(t for t in tareas if t.name == "Integración")
        self.assertEqual(tarea_cargada.progress, 50)
        
    def tearDown(self):
        # Limpieza: eliminar archivo de prueba
        import os
        if os.path.exists("test_integration.json"):
            os.remove("test_integration.json")
