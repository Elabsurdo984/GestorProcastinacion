import unittest
import json
import os
from datetime import datetime, timedelta
from src.storage import Storage
from src.task import Task, Priority

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_tasks.json"
        self.storage = Storage(self.test_file)
        # Usamos una fecha futura para evitar el error de validación
        self.future_date = datetime.now() + timedelta(days=1)
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_guardar_y_cargar_tareas(self):
        tarea = Task("Test", "Desc", self.future_date, Priority.MEDIA)
        self.storage.save_task(tarea)
        tareas = self.storage.load_tasks()
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0].name, "Test")

    def test_actualizar_tarea(self):
        tarea = Task("Test", "Desc", self.future_date, Priority.MEDIA)
        self.storage.save_task(tarea)
        tarea.update_progress(75)
        self.storage.update_task(tarea)
        tareas = self.storage.load_tasks()
        self.assertEqual(tareas[0].progress, 75)